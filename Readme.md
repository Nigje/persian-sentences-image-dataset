# Persian Sentences Image Dataset

A legacy synthetic Persian OCR dataset with clean and noisy single-line sentence
images in eleven fonts. The original generation code and sentence source are not
available. This repository now includes an archive audit, machine-readable labels,
fixed sentence splits, validation tools, and a separate reproducible renderer.

## Dataset at a glance

The dataset contains Persian sentences rendered as single-line images in 11 fonts.
Each usable sample has a clean image, a noisy version, and a text file describing
the characters and their horizontal positions.

| What is included | Amount |
| --- | ---: |
| Fonts | 11 |
| Different Persian sentences | 265 |
| Usable images | 5,822 |
| Clean images | 2,911 |
| Noisy images | 2,911 |
| Total ZIP download size | About 846 MB |

The suggested split assigns **213 sentences to training**, **31 to validation**,
and **21 to testing**. All images of the same sentence stay in the same group,
including different fonts and noisy versions.

Not every font contains every sentence: Arial, Calibri, Tahoma, and Times New Roman
each contain 264 sentences, while the seven B fonts each contain 265.
Sentence texts were recovered from the character annotation files.

The Tahoma archive also contains one extra image that cannot be opened and has no
label. It is excluded from the usable-image counts above. Details are recorded in
[data/audit.json](data/audit.json).

Clean images are PNG files; noisy images are JPEG files. Image sizes vary.
The repository also includes 30 noise backgrounds in `Noises/`, but the original
background used for each noisy image is unknown.

## Download dataset

Download the dataset from [release v1.0.0](https://github.com/Nigje/persian-sentences-image-dataset/releases/tag/v1.0.0).
Download all eleven ZIPs for the complete dataset, or select a font:

```bash
python -m pip install .
python scripts/download.py --font "B Homa"
```

Omit `--font` to download every archive. Downloads are saved locally under
`Dataset/`, which is ignored by Git. The downloader verifies SHA-256 and sizes
against `data/audit.json` and maps original filenames to GitHub's release asset names.
Release metadata includes labels, checksums, the audit, character inventory, and splits.

## Git history migration

Archive history cleanup [completed successfully](https://github.com/Nigje/persian-sentences-image-dataset/actions/runs/36910007819).
ZIPs were removed from both their historical root-level paths and `Dataset/`
across branch and tag history. A verified fresh clone contains no original archive
blobs and its Git pack is 2.59 MiB, compared with approximately 809 MiB before cleanup.
The release archives are unchanged.

The original repository backup is available for seven days in the
[first cleanup run](https://github.com/Nigje/persian-sentences-image-dataset/actions/runs/36909504209)'s artifacts.
Existing clones should be replaced with fresh clones to avoid restoring old history.
The cleanup workflow is now manual-only and does not run on normal pushes.
GitHub retains protected old pull-request refs and may retain cached old objects;
those references are outside ordinary branch/tag cleanup and normal Git pushes.

## Metadata and evaluation

`data/metadata.csv` contains archive-relative image and annotation paths, sentence
ID, literal text, font, variant, noise identity (unknown for legacy noisy samples),
clean counterpart, dimensions, image status, and split. Extract each ZIP preserving
its internal paths. `data/sentences.tsv` stores reconstructed transcriptions.
Sentence IDs are SHA-256 hashes of exact UTF-8 labels, with no Unicode normalization.

Splits use a fixed salted hash with approximately 80/10/10 allocation. Identical
transcriptions stay together across fonts and noise variants. Split files contain
sentence IDs, not image filenames. Filter the manifest by `split`, and use only
`image_status=valid` records. These splits measure generalization to held-out text
within the existing fonts; similar sentences may remain across splits.

Rebuild metadata and validate it:

```bash
python -m pip install .
python scripts/index_dataset.py --archives Dataset --output data
python scripts/validate_dataset.py
python -m unittest discover -s tests
```

Python 3.10+ and Pillow are required. The indexer verifies ZIP CRCs and reads image
headers, but does not guarantee that every image fully decodes or that labels are
visually correct. The audit records known failures instead of silently dropping them.

## Annotation format

Actual UTF-8 rows use `_character_start_end`, including the leading underscore:

```text
_ز_3375_3459
_ی_3333_3375
_ _3171_3214
```

Spaces are literal U+0020 characters. Rows are preserved in source order.
Horizontal intervals are not two-dimensional glyph boxes. Endpoint inclusivity,
ligature mapping, and the original alignment method are unverified; see
[annotation specification](docs/annotation-format.md).

### Character boundaries

The red lines in these original examples mark the start and end of each character's
horizontal interval.

<p align="center">
  <img src="Sample Images/Chunked sentence.jpg" alt="Persian sentence with character boundaries marked by red lines">
</p>

<p align="center">
  <img src="Sample Images/Chunked characters.jpg" alt="Individual Persian characters showing their horizontal boundaries">
</p>

### Sliding-window example

The original illustration below shows the sentence divided into 10-pixel-wide
windows for sequential OCR processing.

<p align="center">
  <img src="Sample Images/Window 10px.png" alt="Persian sentence divided into 10-pixel-wide windows" width="80%">
</p>

## Render a new sample

Supply a font you are permitted to use. Pillow must support RAQM for Persian shaping:

```bash
python scripts/render.py --text "سلام دنیا" --font /path/to/font.ttf --output generated/sample.png --seed 42 --noise 0.01
```

This creates a shaped RTL image and a JSON sentence label. Optional seeded
salt-and-pepper noise is reproducible. This new renderer does not recreate the
legacy fonts, background composition, or character annotations. No font binaries
are distributed. The original generation process cannot be recovered from images
alone.

## Licensing and citation

Licensing remains pending at the maintainer's request. No data or third-party asset
reuse license is granted by this update. See [rights status](docs/rights.md).
`CITATION.cff` supplies a repository citation; cite [release v1.0.0](https://github.com/Nigje/persian-sentences-image-dataset/releases/tag/v1.0.0) when using these data.

## Limitations and intended use

Use for exploratory Persian OCR and controlled synthetic-image experiments.
265 underlying transcriptions provide limited linguistic diversity, regardless of
augmentation. This is not a representative real-document benchmark. Source labels
are reconstructed, noise identities are unknown, and annotation geometry is
unverified. Before broader benchmarking, expand and review the corpus to cover
Persian digits, punctuation, ZWNJ, Arabic/Persian codepoint variants, and optional
diacritics, and validate against real scanned documents. The character inventory
reflects observed labels only.

## Samples

Additionally, various fonts have been showcased in the images to illustrate font diversity within the dataset. For the following samples, the belongs text file is like the following.

```text
_ز_3375_3459
_ی_3333_3375
_ر_3250_3333
_ا_3214_3250
_ _3171_3214
```

See [the annotation specification](docs/annotation-format.md) for parsing and limitations.






### Times New Roman

<p align="center">
  <img  src="Sample Images/Times New Roman.png" alt="Times New Roman" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/Times New Roman_Noise.jpg" alt="Times New Roman" style="width:80%">
    <br/>
	Times New Roman
</p>







### B Mitra

<p align="center">
  <img  src="Sample Images/B Mitra.png" alt="B Mitra" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Mitra_Noise.jpg" alt="B Mitra" style="width:80%">
    <br/>
    B Mitra
</p>







### Tahoma

<p align="center">
  <img  src="Sample Images/Tahoma.png" alt="Tahoma" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/Tahoma_Noise.jpg" alt="Tahoma" style="width:80%">
    <br/>
    Tahoma
</p>







### Arial

<p align="center">
  <img  src="Sample Images/Arial.png" alt="Arial" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/Arial_Noise.jpg" alt="Arial" style="width:80%">
    <br/>
    Arial
</p>







### B Homa

<p align="center">
  <img  src="Sample Images/B Homa.png" alt="B Homa" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Homa_Noise.jpg" alt="B Homa" style="width:80%">
    <br/>
    B Homa
</p>







### B Nazanin

<p align="center">
  <img  src="Sample Images/B Nazanin.png" alt="B Nazanin" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Nazanin_Noise.jpg" alt="B Nazanin" style="width:80%">
    <br/>
    B Nazanin
</p>







### B Traffic

<p align="center">
  <img  src="Sample Images/B Traffic.png" alt="B Traffic" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Traffic_Noise.jpg" alt="B Traffic" style="width:80%">
    <br/>
    B Traffic
</p>







### B Lotus

<p align="center">
  <img  src="Sample Images/B Lotus.png" alt="B Lotus" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Lotus_Noise.jpg" alt="B Lotus" style="width:80%">
    <br/>
    B Lotus
</p>







### B Yagut

<p align="center">
  <img  src="Sample Images/B Yagut.png" alt="B Yagut" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Yagut_Noise.jpg" alt="B Yagut" style="width:80%">
    <br/>
    B Yagut
</p>







### B Zar

<p align="center">
  <img  src="Sample Images/B Zar.png" alt="B Zar" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/B Zar_Noise.jpg" alt="B Zar" style="width:80%">
    <br/>
    B Zar
</p>







### Calibri

<p align="center">
  <img  src="Sample Images/Calibri.png" alt="Calibri" style="width:80%">
</p>
<p align="center">
  <img  src="Sample Images/Calibri_Noise.jpg" alt="Calibri" style="width:80%">
    <br/>
    Calibri
</p>

