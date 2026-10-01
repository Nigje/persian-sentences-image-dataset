# Legacy character annotations

The actual UTF-8 files use `_character_start_end`, including a leading underscore.
For example, `_ز_3375_3459` and `_ _3171_3214`. A space is a literal U+0020
between the first two underscores. Do not trim each line before parsing.
Rows follow transcription order in the inspected sample, with descending horizontal
coordinates for the Persian sentence. Preserve the characters and row order exactly.

These are horizontal intervals, not two-dimensional bounding boxes. Adjacent intervals
can share an endpoint. The original implementation is absent: endpoint inclusivity,
coordinate origin, ligature assignment, and whether these are glyph or logical intervals
are unverified. Do not present them as pixel-accurate glyph boxes. The audit flags
intervals outside image width; it does not prove annotation accuracy.

Metadata transcriptions are reconstructed from the character rows; they are not
independently verified original sentence labels. Arabic/Persian forms and ZWNJ are
preserved without normalization. New rendering provides sentence labels only;
character boxes need a separately validated shaping/alignment implementation.
