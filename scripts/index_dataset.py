"""Audit legacy ZIPs and build reproducible metadata without extracting archives."""
import argparse, csv, hashlib, io, json, re, zipfile
from pathlib import Path
from PIL import Image, UnidentifiedImageError


def parse_annotation(raw):
    rows = []
    for line in raw.decode('utf-8-sig').splitlines():
        if not line:
            continue
        match = re.fullmatch(r'_(.*)_(\d+)_(\d+)', line)
        if not match:
            raise ValueError(f'Invalid annotation: {line!r}')
        char, start, end = match.groups()
        if len(char) != 1 or int(start) > int(end):
            raise ValueError(f'Invalid character interval: {line!r}')
        rows.append((char, int(start), int(end)))
    return rows


def build(source, output):
    output.mkdir(parents=True, exist_ok=True)
    records, sentences, archives, issues = [], {}, [], []
    for path in sorted(source.glob('*.zip')):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        archives.append({'filename': path.name, 'bytes': path.stat().st_size, 'sha256': digest})
        with zipfile.ZipFile(path) as z:
            bad = z.testzip()
            if bad:
                raise ValueError(f'CRC failure: {path}: {bad}')
            names = set(z.namelist())
            clean_by_stem = {Path(n).stem:n for n in sorted(names) if Path(n).suffix.lower() in {'.png','.jpg','.jpeg'} and '/NoisilyImages/' not in n}
            labels = {}
            for name in sorted(names):
                if name.endswith('.txt'):
                    rows = parse_annotation(z.read(name))
                    text = ''.join(r[0] for r in rows)
                    sid = hashlib.sha256(text.encode()).hexdigest()
                    sentences[sid] = text
                    labels[Path(name).stem] = (sid, text, name, rows)
            for name in sorted(names):
                if Path(name).suffix.lower() not in {'.jpg', '.jpeg', '.png'}:
                    continue
                stem = Path(name).stem
                if stem not in labels:
                    issues.append({'archive':path.name,'image_path':name,'issue':'missing annotation'})
                    labels[stem] = ('', '', '', [])
                sid, text, annotation, rows = labels[stem]
                status = 'valid'
                try:
                    with Image.open(io.BytesIO(z.read(name))) as im:
                        width, height = im.size
                except (UnidentifiedImageError, OSError):
                    width, height, status = 0, 0, 'unreadable'
                    issues.append({'archive':path.name,'image_path':name,'issue':'unreadable image'})
                noisy = '/NoisilyImages/' in name
                clean = clean_by_stem.get(stem, '')
                if any(a < 0 or b > width for _, a, b in rows):
                    issues.append({'archive':path.name,'image_path':name,'issue':'annotation outside image width'})
                records.append(dict(archive=path.name,image_path=name,sentence_id=sid,text=text,font=path.stem,variant='noisy' if noisy else 'clean',noise_type='unknown' if noisy else '',clean_image=clean,annotation_path=annotation,width=width,height=height,image_status=status,split=split(sid) if sid and status=='valid' else 'unassigned'))
    if not records:
        raise ValueError('No images found')
    with (output/'metadata.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator="\n"); w.writeheader(); w.writerows(records)
    with (output/'sentences.tsv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n'); w.writerow(['sentence_id','text']); w.writerows(sorted(sentences.items()))
    (output/'character_set.txt').write_text(''.join(sorted(set(''.join(sentences.values()))))+'\n',encoding='utf-8')
    (output/'splits').mkdir(exist_ok=True)
    for group in ['train','validation','test']:
        (output/'splits'/f'{group}.txt').write_text(''.join(s+'\n' for s in sorted(sentences) if split(s)==group))
    (output/'SHA256SUMS.txt').write_text(''.join(f"{a['sha256']}  {a['filename']}\n" for a in archives))
    report={'archives':archives,'images':len(records),'unique_sentences':len(sentences),'annotations':len({(r['archive'],r['annotation_path']) for r in records if r['annotation_path']}),'variants':{v:sum(r['variant']==v for r in records) for v in ['clean','noisy']},'sentence_splits':{g:sum(split(s)==g for s in sentences) for g in ['train','validation','test']},'issues':issues}
    (output/'audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'archives','issues'}},indent=2)); print('Issues:',len(issues))


def split(sid):
    bucket=int(hashlib.sha256(('persian-sentences-v1:'+sid).encode()).hexdigest()[:8],16)%100
    return 'train' if bucket<80 else 'validation' if bucket<90 else 'test'

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--archives',type=Path,default=Path('Dataset')); p.add_argument('--output',type=Path,default=Path('data')); a=p.parse_args(); build(a.archives,a.output)
