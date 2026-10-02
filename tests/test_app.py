import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app


class TestInstagramReportAssistant(unittest.TestCase):

    def test_valid_username(self):
        self.assertTrue(
            app.valid_username("instagram")
        )

        self.assertTrue(
            app.valid_username("@test.user")
        )

        self.assertTrue(
            app.valid_username("test_user123")
        )

    def test_invalid_username(self):
        self.assertFalse(
            app.valid_username("user name")
        )

        self.assertFalse(
            app.valid_username("user/name")
        )

        self.assertFalse(
            app.valid_username("")
        )

    def test_next_draft_id(self):
        drafts = [
            {"id": 1},
            {"id": 5},
            {"id": 10},
        ]

        self.assertEqual(
            app.next_draft_id(drafts),
            11,
        )

    def test_next_id_empty(self):
        self.assertEqual(
            app.next_draft_id([]),
            1,
        )

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)

            with patch.object(
                app,
                "DATA_DIR",
                temp_path,
            ), patch.object(
                app,
                "DRAFTS_FILE",
                temp_path / "reports.json",
            ):

                records = [
                    {
                        "id": 1,
                        "username": "example",
                        "reason": "Spam or scam",
                    }
                ]

                app.save_drafts(records)

                loaded = app.load_drafts()

                self.assertEqual(
                    loaded,
                    records,
                )


if __name__ == "__main__":
    unittest.main()
