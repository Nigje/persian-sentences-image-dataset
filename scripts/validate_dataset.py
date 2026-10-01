"""Validate checked-in manifest, sentence IDs, and leakage-free split membership."""
import csv, hashlib, json
from pathlib import Path
from index_dataset import split
root=Path('data')
with (root/'sentences.tsv').open(encoding='utf-8',newline='') as f:
    sentences={r['sentence_id']:r['text'] for r in csv.DictReader(f,delimiter='\t')}
for sid,text in sentences.items():
    assert hashlib.sha256(text.encode()).hexdigest()==sid, 'Sentence hash mismatch'
sets={g:set((root/'splits'/f'{g}.txt').read_text().splitlines()) for g in ['train','validation','test']}
assert set.union(*sets.values())==set(sentences), 'Incomplete split coverage'
assert all(not sets[a]&sets[b] for a,b in [('train','test'),('train','validation'),('validation','test')]), 'Split leakage'
for g,ids in sets.items():
    assert all(split(s)==g for s in ids), 'Incorrect split assignment'
with (root/'metadata.csv').open(encoding='utf-8',newline='') as f:
    rows=list(csv.DictReader(f))
keys=set()
for r in rows:
    if r['image_status']=='unreadable':
        assert r['split']=='unassigned' and int(r['width'])==0 and int(r['height'])==0
        continue
    if not r['sentence_id']:
        assert r['split']=='unassigned' and not r['annotation_path']
        continue
    assert r['text']==sentences[r['sentence_id']]
    assert r['sentence_id'] in sets[r['split']]
    assert int(r['width'])>0 and int(r['height'])>0
    key=(r['archive'],r['image_path']); assert key not in keys; keys.add(key)
    assert r['annotation_path']
report=json.loads((root/'audit.json').read_text())
assert len(rows)==report['images']
assert len(sentences)==report['unique_sentences']
print(f'Validated {len(rows)} image records and {len(sentences)} sentences; no exact-transcription split leakage.')
