from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sow_build  # noqa: E402
import sow_extract  # noqa: E402


class SOWRuntimeTests(unittest.TestCase):
    def test_default_spec_resolves_outside_plugin_cwd(self) -> None:
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            try:
                spec = sow_build.load_spec()
            finally:
                os.chdir(previous)
        self.assertEqual(spec["page"]["width_in"], 8.5)
        self.assertIn("signature_caption", spec["roles"])

    def test_builder_substitutes_footer_and_inserts_page_field(self) -> None:
        content = sow_build._smoke_content("Acme Corp", "BrightWay AI")
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "sow.docx"
            sow_build.build_from_content(content, output)
            with zipfile.ZipFile(output) as archive:
                footer = archive.read("word/footer1.xml").decode("utf-8")
        self.assertIn("Acme Corp", footer)
        self.assertIn("BrightWay AI", footer)
        self.assertIn("PAGE", footer)
        self.assertNotIn("{client}", footer)
        self.assertNotIn("{vendor}", footer)

    def test_extractor_captures_section_body_and_effective_style(self) -> None:
        content = {
            "client": "Acme Corp",
            "vendor": "BrightWay AI",
            "sections": [
                {
                    "heading": "Relationship of the Parties",
                    "blocks": [
                        {
                            "type": "paragraph",
                            "text": "This approved paragraph must survive extraction.",
                        },
                        {
                            "type": "table",
                            "header": ["Phase", "Cap"],
                            "rows": [["One", "$10,000"]],
                        },
                    ],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "sow.docx"
            sow_build.build_from_content(content, output)
            extracted = sow_extract.extract(output)
        self.assertEqual(len(extracted["sections"]), 1)
        self.assertEqual(extracted["sections"][0]["heading"], "Relationship of the Parties")
        self.assertEqual(
            extracted["sections"][0]["body"],
            ["This approved paragraph must survive extraction."],
        )
        self.assertTrue(extracted["roles"]["section_heading"]["bold"])
        self.assertIsNotNone(extracted["roles"]["body"]["name"])
        self.assertEqual(extracted["roles"]["body"]["color"], "000000")
        self.assertEqual(extracted["roles"]["table_header"]["size_pt"], 10.0)
        self.assertTrue(extracted["roles"]["table_header"]["bold"])
        self.assertIn("{page}", extracted["footer_text"])

    def test_structured_content_rejects_ragged_table_rows(self) -> None:
        document = sow_build.SOWDoc()
        with self.assertRaisesRegex(ValueError, "expected 2"):
            document.table(["A", "B"], [["only one cell"]])

    def test_user_spec_deep_merges_with_packaged_default(self) -> None:
        custom = {
            "page": {"margin_top_in": 0.75},
            "roles": {"body": {"name": "Arial"}},
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "template.md"
            path.write_text(
                "# Template\n\n```json\n" + json.dumps(custom) + "\n```\n",
                encoding="utf-8",
            )
            spec = sow_build.load_spec(path)
        self.assertEqual(spec["page"]["margin_top_in"], 0.75)
        self.assertEqual(spec["page"]["margin_left_in"], 1)
        self.assertEqual(spec["roles"]["body"]["name"], "Arial")
        self.assertEqual(spec["roles"]["body"]["size_pt"], 11)


if __name__ == "__main__":
    unittest.main()
