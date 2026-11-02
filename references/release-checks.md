# Release checks

Use this checklist against the actual output. Fix failures across the whole pack, not only on the user's marked page.

## Content and paper

- Official chapter/subtopic order and learning-standard coverage are traceable.
- Every selected translation is complete and uses the intended Chinese script.
- Student and teacher questions share IDs, options and answer meanings.
- Student editions have no reference appendix or answer key; teacher references remain.
- All pages were inspected for clipped text, overflow, repeated titles, footer drift, blank pages, missing images and poorly used space.
- Every MCQ has at least four well-spaced choices; each complete question stays together.
- Every scientific label endpoint and diagram was checked against appropriate references.

## Classroom

- The displayed page is the actual final student PDF, including continuation pages.
- Every blank/choice overlay matches the intended place at full-page, page-width and enlarged zoom.
- Space/Right reveals until the end, then advances a page. Left hides until zero, then goes back. First/last boundaries stop.
- Returning to a page preserves its reveal state. Button labels and enabled states match keyboard behavior.
- Key repeat does not race through pages. Typing or working in dialogs does not change the lesson.
- Fast page/language changes cannot display a stale decoded image with current answers.
- Transitions work, with reduced-motion alternatives. Page images are decoded before swapping.
- Check normal and enlarged text/labels, not only a thumbnail. Measure the rendered image dimensions; don't infer resolution from the file name.
- Notes, marks, export/import and reload preserve the right course/page/language data. Touch drawing is opt-in so scrolling is still possible.
- Video/activity controls are shown only when the lesson has that material. Verify links and embedded playback where practical; provide a source link fallback for blocked embeds.

## If online saving is requested

- A user-scoped record is saved and read back through the real service where authorized.
- Separate-context tests distinguish cloud readback from local browser storage.
- Authentication failure, account change, offline drafts and conflicts preserve user data.
- A migration uses a separate state key or a verified conversion. Preserve old unsynced drafts.
- Never inspect other students' progress merely to verify the feature.

## If publishing is requested

- Confirm the destination and scope from the user's instruction; don't create an account platform just for a static HTML pack.
- Inspect the final file list. Include only approved reusable files and example assets. Check public packages for secrets, personal paths, internal service IDs and private source documents.
- Check file-size limits on the actual host. The example's maximum is configurable; 50 MiB is not a universal limit.
- Preserve other modules and current live updates. Prefer replacing the exact course artifact over redeploying a stale whole-site checkout.
- Verify the live route and one full interaction after publishing. Distinguish local checks, mocked-service tests and real live checks in the handoff.
- Report the deliverable links and any practical unverified condition once. Do not claim physical iPad/Pencil testing from a desktop viewport.
