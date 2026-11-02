# Presenter data and implementation

## Portable build

Install the pinned Python dependencies from `requirements.txt`, then run:

```sh
python scripts/build_classroom.py examples/eye-detecting-light/course.json classroom.html --width 2380 --max-mib 49
```

Open the resulting HTML in a current desktop browser. The file embeds its page images and runtime. Core page/reveal behavior works without a server. Optional YouTube playback needs a network connection.

The helper accepts an existing reviewed PDF and measured answer coordinates. It does not generate the chapter content or guess geometry. Use its example manifest as the concrete schema reference.

## Manifest shape

```json
{
  "schemaVersion": 1,
  "id": "science-light-sample-v1",
  "title": {"en": "Light and vision", "zh": "光与视觉"},
  "defaultLanguage": "en-zh",
  "sections": [{"id": "1.2", "title": {"en": "Vision", "zh": "视觉"}}],
  "lessons": [{"id": "1.2-01", "section": "1.2", "title": {"en": "Detecting light", "zh": "感知光线"}}],
  "languages": {
    "en-zh": {
      "label": "English + 简体中文",
      "pdf": "student-en-zh.pdf",
      "pages": [{
        "lessonId": "1.2-01",
        "section": "1.2",
        "steps": [
          {"kind": "blank", "items": [{"x": 0.2, "y": 0.5, "w": 0.16, "h": 0.02, "font": 0.018, "text": "retina"}]},
          {"kind": "choice", "answer": "B", "items": [{"x": 0.52, "y": 0.7, "w": 0.35, "h": 0.05, "font": 0.018}]}
        ]
      }]
    }
  }
}
```

The numbers above only illustrate the fields. They do not locate answers on the included PDF. Never reuse these coordinates without measuring a real page.

- `id` is a unique course/content identity used for storage. Reuse it for compatible corrections; define a migration or new identity when page-based data becomes incompatible. Do not inherit the sample ID for another course.
- `title`, section titles and lesson titles are translation objects. Language labels and available modes come from the manifest.
- Each language has its own reviewed PDF and physical page list, in PDF order. Include continuation pages and pages with no answer steps. Page counts need not match across languages.
- `lessonId` can repeat across continuation pages. It is not a physical page index.
- Every overlay rectangle is relative to the page's visible width/height, with a **top-left** origin. `font` is the font size divided by page width.
- All coordinates must be inside the page. Convert PDF bottom-left coordinates before using them. If the PDF has rotation/cropping, measure the displayed crop and orientation used by the renderer.
- One blank step may contain both English and Chinese rectangles. Reveal them together.
- A choice step highlights the full correct choice region, including its translation. It does not retype or replace the question.
- Page images are produced by the build, not supplied as a second independent source of truth.

For print HTML, capture final page/blank rectangles **after** fonts load, images decode, print media applies and pagination finishes. Normalize against each physical sheet. Verify the PDF has the same page count, dimensions and layout. Any change to pagination requires new geometry and review.

## Runtime model

Keep one state object for the current course, language, physical page, zoom and maps of per-page reveal counts, notes, marks and drawings. The included viewer uses `language:pageIndex` keys. That is safe only while the page sequence stays compatible; a new content revision must migrate or isolate page-based state.

When switching language, map to the same lesson when available rather than assuming the same page number. Preserve the separate reveal history and marks for each language. Never stretch a mark from one language's layout onto another.

The public example is local-only. It does not contain an account backend or publishing destination. Its presenter API supports integration, but an account adapter must disable anonymous local restoration, wait for the authenticated state/page to be ready, and lock the surface on account change. Use per-user storage names and retain legacy drafts. Apply remote state without recursively writing it back as a new edit.

## Resolution and delivery size

2380 px wide with WebP quality 86 was accepted for this teaching workflow at 150% page-width zoom. It is a baseline, not a universal promise for every projector or retina display. Inspect text and line labels at the actual target zoom. Do not upscale a small screenshot and call it a high-resolution PDF render.

If a host limit is exceeded, first measure the actual built bytes and inspect which assets dominate. Prefer splitting delivery by language, adaptive rendering or a suitable PDF renderer when needed. Lower resolution only when it still meets the user's display needs, and state the tradeoff. The command's 49 MiB limit is configurable and leaves room under the original host's 50 MiB limit; it is not a restriction on the teaching workflow.

## Transition rules

Decode the target image while keeping the current page visible. Commit the new image, overlays and page identity together. Use a monotonically increasing render request ID or equivalent cancellation so an old asynchronous decode cannot win a later navigation. Keep the animation short and ignore held-key repeat. In reduced-motion mode, show the page without movement. Do not use page-turn effects that make scientific text harder to read.
