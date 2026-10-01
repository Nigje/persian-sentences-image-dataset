"""Stage ZIP removal only when a published release has matching assets."""
import json, subprocess
from pathlib import Path
repo='Nigje/persian-sentences-image-dataset'
release=json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/releases/tags/v1.0.0']))
if release['draft']:
    raise SystemExit('Release is still a draft; refusing removal')
assets={a['name']:a for a in release['assets']}
for expected in json.loads(Path('data/audit.json').read_text())['archives']:
    asset=assets.get(expected['filename'])
    if not asset or asset['size']!=expected['bytes'] or asset['state']!='uploaded':
        raise SystemExit(f"Missing/incomplete release asset: {expected['filename']}")
    if asset.get('digest') and asset['digest']!='sha256:'+expected['sha256']:
        raise SystemExit(f"Release digest mismatch: {expected['filename']}")
if 'SHA256SUMS.txt' not in assets:
    raise SystemExit('Missing release checksums')
subprocess.run(['git','rm','--',*[str(p) for p in sorted(Path('Dataset').glob('*.zip'))]],check=True)
print('ZIP deletions staged. Review and commit them; shared Git history remains intact.')
