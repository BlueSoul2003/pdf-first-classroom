import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('builder', ROOT / 'scripts/build_classroom.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
EXAMPLE = ROOT / 'examples/eye-detecting-light'


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((EXAMPLE / 'course.json').read_text(encoding='utf-8'))

    def test_manifest_and_actual_pdf_pages(self):
        paths = builder.validate_manifest(self.manifest, EXAMPLE)
        self.assertEqual(set(paths), {'en', 'en-zh', 'zh', 'ms', 'ms-zh'})
        self.assertEqual(len(self.manifest['languages']['en-zh']['pages']), 2)

    def test_page_count_mismatch_fails(self):
        self.manifest['languages']['en']['pages'].pop()
        with self.assertRaisesRegex(ValueError, 'page count differs'):
            builder.validate_manifest(self.manifest, EXAMPLE)

    def test_missing_answer_and_bad_geometry_fail(self):
        item = self.manifest['languages']['en']['pages'][0]['steps'][0]['items'][0]
        item['text'] = ''
        with self.assertRaisesRegex(ValueError, 'blank answer'):
            builder.validate_manifest(self.manifest, EXAMPLE)
        item['text'] = 'optic nerve'
        item['x'] = .99
        with self.assertRaisesRegex(ValueError, 'outside page'):
            builder.validate_manifest(self.manifest, EXAMPLE)

    def test_external_file_rejected(self):
        self.manifest['languages']['en']['pdf'] = '../private.pdf'
        with self.assertRaisesRegex(ValueError, 'inside the manifest'):
            builder.validate_manifest(self.manifest, EXAMPLE)

    def test_render_real_pdf_and_output_cap(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'classroom.html'
            data = builder.build(EXAMPLE / 'course.json', output, width=800)
            self.assertGreater(output.stat().st_size, 100000)
            self.assertEqual(data['languages']['en']['pages'][0]['width'], 800)
            self.assertNotIn('__PRESENTER_DATA__', output.read_text(encoding='utf-8'))
            before = output.read_bytes()
            with self.assertRaisesRegex(ValueError, 'exceeds'):
                builder.build(EXAMPLE / 'course.json', output, width=800, max_mib=.001)
            self.assertEqual(output.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
