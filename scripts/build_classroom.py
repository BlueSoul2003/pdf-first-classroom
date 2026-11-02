"""Render a PDF/answer manifest into one portable, offline classroom HTML."""

import argparse
import base64
import io
import json
import math
import re
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def label(value):
    return isinstance(value, str) and bool(value.strip()) or (
        isinstance(value, dict)
        and bool(value)
        and all(isinstance(v, str) and v.strip() for v in value.values())
    )


def numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_manifest(data, directory):
    require(isinstance(data, dict) and data.get('schemaVersion') == 1, 'schemaVersion must be 1')
    require(bool(re.fullmatch(r'[a-zA-Z0-9_-]{1,100}', data.get('id', ''))), 'Use a unique portable course id')
    require(label(data.get('title')), 'Course title is required')
    sections = data.get('sections')
    lessons = data.get('lessons')
    require(isinstance(sections, list) and sections, 'At least one section is required')
    require(isinstance(lessons, list) and lessons, 'At least one lesson is required')
    section_ids = set()
    for section in sections:
        require(isinstance(section, dict), 'Sections must be objects')
        sid = section.get('id')
        require(isinstance(sid, str) and sid and sid not in section_ids, 'Section IDs must be unique')
        require(label(section.get('title')), 'Section title is required')
        section_ids.add(sid)
    lesson_map = {}
    for lesson in lessons:
        require(isinstance(lesson, dict), 'Lessons must be objects')
        lid = lesson.get('id')
        require(isinstance(lid, str) and lid and lid not in lesson_map, 'Lesson IDs must be unique')
        require(lesson.get('section') in section_ids and label(lesson.get('title')), 'Invalid lesson section/title')
        require(lesson.get('activity') in (None, 'reaction', 'pupil', 'phototropism'), 'Unknown activity')
        video = lesson.get('video')
        if video is not None:
            require(isinstance(video, dict) and bool(re.fullmatch(r'[A-Za-z0-9_-]{11}', video.get('id', ''))) and label(video.get('title')), 'Invalid YouTube video')
        lesson_map[lid] = lesson
    languages = data.get('languages')
    require(isinstance(languages, dict) and languages, 'At least one language is required')
    require(data.get('defaultLanguage') in languages, 'defaultLanguage must exist')
    paths = {}
    for code, language in languages.items():
        require(bool(re.fullmatch(r'[a-z]{2,3}(?:-[a-zA-Z]{2,8})*', code)), 'Invalid language code')
        require(isinstance(language, dict) and isinstance(language.get('label'), str), 'Language label is required')
        require(isinstance(language.get('pdf'), str), 'Each language needs a PDF path')
        pdf = (directory / language['pdf']).resolve()
        require(pdf.is_relative_to(directory.resolve()), 'Keep input PDFs inside the manifest directory')
        require(pdf.is_file() and pdf.suffix.lower() == '.pdf', f'Missing PDF for {code}')
        pages = language.get('pages')
        require(isinstance(pages, list) and pages, f'Missing pages for {code}')
        with pdfium.PdfDocument(str(pdf)) as document:
            require(len(document) == len(pages), f'{code}: PDF page count differs from overlay count')
        for page_index, page in enumerate(pages):
            where = f'{code} page {page_index + 1}'
            require(isinstance(page, dict), f'{where}: page must be an object')
            lesson = lesson_map.get(page.get('lessonId'))
            require(lesson is not None and page.get('section') == lesson['section'], f'{where}: invalid lesson/section')
            require('image' not in page, f'{where}: images are generated from the PDF, not supplied')
            require(isinstance(page.get('steps'), list), f'{where}: steps must be an array')
            for step in page['steps']:
                require(isinstance(step, dict) and step.get('kind') in ('blank', 'choice'), f'{where}: invalid step kind')
                require(isinstance(step.get('items'), list) and step['items'], f'{where}: step needs overlay items')
                if step['kind'] == 'choice':
                    require(isinstance(step.get('answer'), str) and bool(step['answer'].strip()), f'{where}: choice answer is required')
                for item in step['items']:
                    require(isinstance(item, dict), f'{where}: item must be an object')
                    require(all(numeric(item.get(k)) for k in ('x', 'y', 'w', 'h', 'font')), f'{where}: rectangle/font must be finite numbers')
                    require(0 <= item['x'] <= 1 and 0 <= item['y'] <= 1 and item['w'] > 0 and item['h'] > 0 and item['x'] + item['w'] <= 1.00001 and item['y'] + item['h'] <= 1.00001, f'{where}: overlay outside page')
                    require(0 < item['font'] < .25, f'{where}: invalid normalized font size')
                    if step['kind'] == 'blank':
                        require(isinstance(item.get('text'), str) and bool(item['text'].strip()), f'{where}: blank answer is required')
        paths[code] = pdf
    return paths


def build(manifest, output, width=2380, quality=86, max_mib=49):
    require(800 <= width <= 8000, 'Page width must be 800–8000 pixels')
    require(1 <= quality <= 100, 'WebP quality must be 1–100')
    require(numeric(max_mib) and max_mib > 0, 'max-mib must be positive')
    manifest = Path(manifest).resolve()
    data = json.loads(manifest.read_text(encoding='utf-8-sig'))
    paths = validate_manifest(data, manifest.parent)
    for code, language in data['languages'].items():
        with pdfium.PdfDocument(str(paths[code])) as document:
            for index, page_data in enumerate(language['pages']):
                page = document[index]
                bitmap = page.render(scale=width / page.get_width())
                with bitmap.to_pil().convert('RGB') as image:
                    buffer = io.BytesIO()
                    image.save(buffer, 'WEBP', quality=quality, method=6)
                    page_data.update(image='data:image/webp;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii'), width=image.width, height=image.height)
                bitmap.close()
                page.close()
        del language['pdf']
        print(f'{code}: {len(language["pages"])} pages at {width}px')
    data.pop('schemaVersion')
    serialized = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    template = (ROOT / 'assets/presenter.html').read_text(encoding='utf-8')
    script = (ROOT / 'assets/presenter.js').read_text(encoding='utf-8')
    result = template.replace('__PRESENTER_DATA__', serialized).replace('__PRESENTER_JS__', script)
    encoded = result.encode('utf-8')
    require(len(encoded) <= max_mib * 1024 * 1024, f'HTML is {len(encoded) / 1048576:.2f} MiB; exceeds {max_mib} MiB. Split the chapter or select an explicit width/quality tradeoff.')
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encoded)
    print(f'Built {output.name}: {len(encoded)} bytes')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--width', type=int, default=2380)
    parser.add_argument('--quality', type=int, default=86)
    parser.add_argument('--max-mib', type=float, default=49)
    args = parser.parse_args()
    try:
        build(args.manifest, args.output, args.width, args.quality, args.max_mib)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.exit(1, f'Build failed: {error}\n')


if __name__ == '__main__':
    main()
