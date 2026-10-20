# Arachnida

This folder contains the two mandatory programs for the Arachnida project:

- `spider.py`: downloads images from a website (single page or recursive mode).
- `scorpion.py`: inspects image metadata (EXIF and other available fields).

## Requirements

- Python 3
- Packages:
  - `requests`
  - `beautifulsoup4`
  - `Pillow`

Install dependencies:

```bash
/usr/bin/python3 -m pip install requests beautifulsoup4 Pillow
```

## 1) Spider

`spider.py` extracts image URLs from web pages and downloads supported formats:

- `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

### Usage

```bash
/usr/bin/python3 spider.py [-r] [-l N] [-p PATH] URL
```

### Options

- `-r` Enable recursive crawling.
- `-l N` Maximum recursion depth (default: `5`).
- `-p PATH` Output directory for downloads (default: `./data`).

### Behavior

- Without `-r`: processes only the provided page.
- With `-r`: traverses links recursively until depth `-l`.
- Skips duplicate pages and duplicate image URLs.

### Examples

Single page (no recursion):

```bash
/usr/bin/python3 spider.py https://books.toscrape.com/catalogue/category/books/science_22/index.html
```

Recursive crawl, depth 1:

```bash
/usr/bin/python3 spider.py -r -l 1 https://books.toscrape.com/catalogue/category/books/science_22/index.html
```

Custom output directory:

```bash
/usr/bin/python3 spider.py -p ./my_test_data https://books.toscrape.com/catalogue/category/books/science_22/index.html
```

## 2) Scorpion

`scorpion.py` inspects one or more image files and prints:

- Basic file/image metadata (name, path, dimensions, format, mode)
- File timestamps (created, modified)
- EXIF fields (when present)
- Other embedded metadata (when available)

### Usage

```bash
/usr/bin/python3 scorpion.py FILE1 [FILE2 ...]
```

### Validation order

For each input path, `scorpion.py` checks in this order:

1. Supported extension (`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`)
2. File existence
3. Image opening/parsing with Pillow

This means a missing `.txt` file reports unsupported extension first.

### Examples

Inspect one file:

```bash
/usr/bin/python3 scorpion.py ./data/example.jpg
```

Inspect multiple files:

```bash
/usr/bin/python3 scorpion.py ./data/*.jpg
```

Error-handling demo (unsupported + missing file):

```bash
/usr/bin/python3 scorpion.py ./README.md ./no_such_file.jpg ./missing.txt
```

## Notes

- Spider skips duplicate pages and duplicate image URLs.
- Scorpion validates extension first, then file existence, then opening/parsing.
- Both scripts are designed to continue running when a single item fails.

## Project Scope

These scripts are focused on the mandatory project behavior:

- Spider: website image extraction with recursion/depth/path options.
- Scorpion: metadata extraction from image files.

## Quick Evaluation Checklist (42)

Install dependencies:

```bash
/usr/bin/python3 -m pip install requests beautifulsoup4 Pillow
```

Run spider:

```bash
/usr/bin/python3 spider.py -r -l 1 https://books.toscrape.com/catalogue/category/books/science_22/index.html
```

Run scorpion:

```bash
/usr/bin/python3 scorpion.py ./data/*.jpg
```
