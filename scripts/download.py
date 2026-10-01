"""Download published v1.0.0 archives and verify committed SHA-256 digests."""
import argparse, hashlib, json, urllib.parse, urllib.request
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--font',help='Exact font name, e.g. B Homa; omitted downloads all fonts'); p.add_argument('--output',type=Path,default=Path('Dataset')); a=p.parse_args()
archives=json.loads(Path('data/audit.json').read_text())['archives']
if a.font:
    archives=[r for r in archives if r['filename']==a.font+'.zip']
    if not archives: p.error('Unknown font')
a.output.mkdir(parents=True,exist_ok=True)
for r in archives:
    target=a.output/r['filename']; temp=target.with_suffix('.zip.part')
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==r['sha256']:
        print('Verified existing',target); continue
    url='https://github.com/Nigje/persian-sentences-image-dataset/releases/download/v1.0.0/'+urllib.parse.quote(r['filename'])
    try:
        urllib.request.urlretrieve(url,temp)
        if temp.stat().st_size!=r['bytes'] or hashlib.sha256(temp.read_bytes()).hexdigest()!=r['sha256']:
            raise ValueError(f'Checksum/size mismatch: {r["filename"]}')
        temp.replace(target); print('Verified',target)
    finally:
        temp.unlink(missing_ok=True)
