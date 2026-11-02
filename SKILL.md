---
name: pdf-first-classroom
description: Create syllabus-matched student notes, teacher answers, and a high-resolution single-page PDF classroom with in-place answer reveals. Use for chapter teaching packs or converting reviewed worksheets into keyboard-controlled lessons; includes whole-document layout review and reusable examples.
---

# PDF First Classroom

Produce a teaching pack students can follow on paper while the teacher presents the same physical PDF page. Treat the supplied syllabus, textbook edition, audience, language, and existing approved design as the content contract. The user's current instructions override this default workflow.

Read [the accepted example](references/accepted-example.md) when starting a new pack. Read [print and content standards](references/print-and-content.md) before authoring notes, and [the presenter contract](references/presenter-contract.md) before implementing the classroom. Use [the release checks](references/release-checks.md) before delivery.

## Start with the source

Find the existing project and editable sources before creating another copy. Identify subject, level, chapter, textbook edition and page numbering. For KSSM Science, use the official textbook as the primary content and chapter-order reference; cross-check the applicable DSKP learning standards. Supplementary publishers such as Pelangi can clarify a point only after their actual content has been read. Do not present a search listing as a verified source.

Create a compact chapter/subtopic/source map in the existing project record or teacher edition. Keep official chapter and subsection numbering. Distinguish textbook printed page numbers from PDF viewer page numbers. Never invent unavailable textbook contents, syllabus coverage or official answers. If the primary source is missing, progress on structure and ask for the needed source before claiming syllabus alignment.

## Make one coherent teaching pack

Use a shared content source with stable lesson, block and question IDs. Derive student notes, teacher answers and classroom steps from it. Reuse the approved design when revising a chapter; don't restart the layout after each comment.

Default for this KSSM teaching profile:

- Student PDF in English with Simplified Chinese support, plus a separate English-only student PDF.
- Teacher edition with filled answers, answer key and references. Keep reference lists and production notes out of student materials.
- Classroom language modes for English + Simplified Chinese, English, Simplified Chinese, Malay, and Malay + Simplified Chinese when those translations are in scope.
- Short sentences, clear knowledge blocks, useful blanks, relevant pictures and four-option understanding checks.

Other curricula and requested language sets can use the same workflow. Do not translate into languages the user does not need. Audit every selected language separately because translated text changes pagination.

## Author, review, then freeze the print pages

Group each subtopic into readable blocks. Use accurate, age-appropriate visual teaching material. Prefer suitable real photographs; use generated illustrations when an appropriate asset is unavailable. For anatomy, check authoritative scientific diagrams before generation and verify each label afterward. Use gentle, recognizable anatomical teaching models for eyes, ears and related structures; avoid crude abstract substitutes and graphic tissue textures. Put labels on deliberately, rather than trusting generated lettering.

Inspect the entire exported PDF, not just annotated pages. Remove repetitive explanatory captions, repeated continuation-page titles and unused “My explanation / sketch” sections. Fix both footer anchors at the bottom. Where a complete relevant question fits, add a Quick check with at least four spaced options. Preserve readability and keep a question with its options. Do not shrink type or add unrelated filler merely to fill a page.

Finish the student PDF layout before extracting answer coordinates. Re-exporting or repaginating a PDF invalidates its old coordinates until rechecked.

## Present the actual PDF

Use one physical student PDF page at a time as the main teaching surface. Put answers over the matching blank or choice. Keep video, activities, notes and drawing tools behind concise controls or dialogs. No permanent second teaching pane or opening dashboard.

The accepted keyboard behavior is:

| Input | Current page has another answer step | At the page boundary |
|---|---|---|
| Space or Right arrow | Reveal the next step | After all steps are visible, the next press opens the next page |
| Left arrow | Hide the last visible step | At zero visible steps, the next press opens the previous page |

Keep each page's reveal count when returning. Stop at the first and last page. Ignore held-key repeat and keep normal input behavior in text fields, selectors and dialogs. Make visible buttons agree with keyboard behavior.

Use a gentle roughly 180–220 ms transition. Decode a new page before swapping it in, and prevent a late image load from replacing a newer page. Respect reduced-motion preferences. Use normalized page coordinates so answers and marks stay aligned during zoom. A bilingual pair for one blank is one reveal step; each multiple-choice question is one step.

Use the actual PDF at sufficient resolution for the intended zoom. The accepted raster baseline is 2380 px wide, verified at 150% page-width zoom. For larger displays or zoom, use higher resolution, adaptive PDF rendering or vector text. Do not promise unlimited sharpness from a fixed raster image or silently trade away legibility to meet a file-size limit.

## Build from the included working example

Use `scripts/build_classroom.py` and `assets/` as a portable starting point, not a fixed Chapter 1 application. The manifest supplies course identity, title, languages, PDF files, physical pages and answer geometry. See [the manifest and build contract](references/presenter-contract.md).

The build helper converts reviewed PDFs and already-verified coordinates into a self-contained classroom. It does not write the syllabus, discover correct answers or automatically recover blank positions from arbitrary PDFs. Extract positions from your final print DOM or another measured PDF layout, then check them against the actual rendered pages.

Keep all local paths and platform credentials outside reusable content. Rebuild and test the actual artifact after changing content, coordinates or runtime code.

## Save and deliver honestly

Local HTML may save page, language, zoom, answers, notes and drawings in the current browser, with export/import where practical. Use a unique course ID; preserve existing user work during updates.

Cloud accounts and publishing are optional. If requested, use the user's existing platform and authorization. Keep per-user drafts isolated, preserve offline work and resolve conflicting edits explicitly. A new UI state model must not overwrite old unsynced drafts. Local reload is not evidence of cross-device cloud sync.

Deliver usable student PDFs, teacher PDF, classroom HTML and editable sources. State where to open them and the short keyboard controls. Publish only when authorized, to the requested destination and audience; verify the live artifact afterward. A request to create a classroom is not permission to publish its source PDFs publicly.

For a public workflow repository, include only approved examples, reusable code and asset provenance. Exclude private teaching libraries, account records, credentials, internal deployment IDs and host-specific paths. Record actual checks and remaining limitations without claiming physical tablet or cross-device tests that were not run.
