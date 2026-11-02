# Accepted example and revision lessons

This skill grew from an iterated KSSM Form 3 Science Chapter 1 teaching pack. It preserves the teacher's accepted output requirements, rather than requiring future teachers to rediscover them through repeated PDF annotations.

The included eye/retina example is a short excerpt of original teaching notes from that pack. It is not a scan of an official textbook, a complete chapter, or an official answer scheme. Its cutaway is an AI-generated teaching illustration with deliberately placed labels. The original lesson was checked against textbook content and National Eye Institute structure references. Scientific review remains necessary when adapting it.

## What changed during review

| Observed problem | Accepted correction | Reusable check |
|---|---|---|
| A selected page contained a redundant anatomical-image explanation | Remove the repeated caption from the entire pack | Search all editions and inspect representative output pages |
| A footer appeared halfway down a short page | Keep left and right footer items at the physical page bottom | Check short notes pages and long continuation pages |
| Continuation pages repeated the large lesson title | Keep the large title at its first occurrence | Inspect every continuation page |
| An anatomical image was too graphic for secondary students | Use a gentler teaching model without losing structure accuracy | Check age suitability and every label endpoint separately |
| Questions had fewer than four options or cramped spacing | Use at least four choices and comfortable padding | Count options and review actual page geometry |
| Empty “My explanation / sketch” areas wasted paper | Remove them throughout | Review all languages and editions |
| Only annotated pages received more questions | Sweep the entire document for space that fits a complete relevant Quick check | Include notes pages and exercise continuation pages |
| Student notes contained a reference appendix | Keep reference material in the teacher edition | Inspect each student PDF's final page |
| The web lesson used a left/right split, making paper harder to follow | Show the actual student PDF one physical page at a time | Compare classroom page IDs with the exported PDF |
| Arrow keys stopped after showing all answers | Continue into the next page on the next press; reverse after hiding all answers | Test both directions and end-of-book boundaries |
| Enlarged pages became soft | Re-render from the PDF at 2380 px width and inspect 150% zoom | Measure natural image size and read enlarged text/labels |
| A new viewer reused the old draft storage key | Isolate the new state and retain old unsynced drafts | Seed an old draft and verify it survives the upgrade |

## Expected outcome

The teacher presses Space or Right to reveal a blank/answer on the same page students have on paper. After the last answer, the next press turns the page with a short gentle transition. Left reverses the reveal sequence, then returns to the previous page. Page history remains intact. Video, notes and drawing tools are available without taking half the teaching surface.

The full original pack had 27 lessons, not 27 physical pages. Its bilingual student edition had 38 pages and its English-only edition had 30. These counts illustrate why the viewer must follow actual PDF pages. They are not constants to copy into a new chapter.

The short public example has 2/2/1/2/2 pages in English + Chinese, English, Chinese, Malay and Malay + Chinese. Its printed running header retains the original lesson position, while the viewer numbers only the excerpt's physical pages. Core learning points and the original check are shared; supplemental checks follow the reviewed print layout and can differ in number. Teacher/student question matching is checked within the same language. Do not silently drop required concepts or core questions to make a translation fit.

`lesson-content.json` is editable wording, while `print-source.html` is the editable layout snapshot. They are not automatically linked. After editing, synchronize the content and layout, export the revised PDF, remeasure overlays and run the release checks. The supplied builder starts after those authoring steps.

## Try a new chapter

Example request for an AI with access to the needed textbook:

> Use $pdf-first-classroom for KSSM Form 3 Science Chapter 2. Use the supplied official textbook edition and its actual subtopics. Produce English + Simplified Chinese student notes, a separate English-only student PDF, and teacher answers with references. Build the same single-page classroom with in-place answers, continuous Space/arrow navigation and readable enlarged pages. Review every PDF page before delivery. Keep this chapter local until I request publishing.

Example request when a reviewed PDF already exists:

> Use $pdf-first-classroom to turn this student PDF and answer key into a classroom. Keep the PDF layout, use one physical page at a time, and place answers exactly over the blanks or correct choices. Make Right/Space reveal then advance, and Left hide then return. Keep the supplied language only. Verify 150% zoom and save/reload. Do not add an account system.

## Content references for the example

- KPM/Sasbadi, *Science Form 3*, 2019, ISBN 978-983-77-0874-7. Publisher preliminaries/contents: https://sasbadisb.com/download/preliminaries.pdf . Obtain the actual authorized textbook for chapter authoring; the contents alone cannot verify a lesson.
- National Eye Institute, *About the Eye*: https://www.nei.nih.gov/eye-health-information/healthy-vision/nei-for-kids/about-eye . Supports anatomical structure and function checks; no NEI diagram is bundled as the example's artwork.

Keep these references in teacher/source documentation. New subjects need their own authoritative references, not this eye bibliography copied forward.
