"""Kör med: python -m unittest -v."""

import unittest
from pathlib import Path

import pandas as pd
from streamlit.testing.v1 import AppTest

from app import MAX_FILE_BYTES, load_csv, summarize_columns


APP_PATH = Path(__file__).with_name("app.py")
SAMPLE = Path(__file__).with_name("sample_data.csv").read_bytes()


class DataTests(unittest.TestCase):
    def test_sample_values_types_and_statistics(self):
        data = load_csv(SAMPLE)
        self.assertEqual(data.shape, (12, 4))
        self.assertEqual(data.iloc[0]["produkt"], "Anteckningsbok")
        self.assertTrue(pd.api.types.is_numeric_dtype(data["pris"]))
        summary = summarize_columns(data)
        self.assertEqual(summary["Saknade värden"].to_dict(),
                         {"produkt": 0, "kategori": 1, "pris": 1, "antal": 1})
        self.assertEqual(summary.loc["pris", "Saknade (%)"], 8.3)
        stats = data["pris"].describe()
        self.assertEqual(stats["count"], 11)
        self.assertEqual(stats["50%"], 79)
        self.assertAlmostEqual(stats["mean"], 945 / 11)

    def test_semicolon_decimal_comma_and_bom(self):
        data = load_csv("\ufeffnamn;pris\nSkål;12,5\n".encode("utf-8"), ";", ",")
        self.assertEqual(data.loc[0, "namn"], "Skål")
        self.assertEqual(data.loc[0, "pris"], 12.5)

    def test_quoted_separator_and_missing_value(self):
        data = load_csv(b'name,value\n"a,b",2\nc,\n')
        self.assertEqual(data.loc[0, "name"], "a,b")
        self.assertTrue(pd.isna(data.loc[1, "value"]))

    def test_invalid_files(self):
        invalid_files = [b"", b" \n", b"a,b\n", b'a,b\n"unfinished,1',
                         b"a,b\n1,2,3\n", b"a,b\n1\n", b"a,a\n1,2\n",
                         b",b\n1,2\n", b"a\n\xff", b"a\n\x00"]
        for content in invalid_files:
            with self.subTest(content=content):
                with self.assertRaises(ValueError):
                    load_csv(content)

    def test_size_limit(self):
        with self.assertRaisesRegex(ValueError, "för stor"):
            load_csv(b"a" * (MAX_FILE_BYTES + 1))


class AppTests(unittest.TestCase):
    def run_upload(self, content):
        # AppTest simulerar widgeten, inte webbläsarens filväljare.
        app = AppTest.from_file(str(APP_PATH), default_timeout=20).run()
        app.file_uploader[0].set_value(("test.csv", content, "text/csv")).run()
        self.assertEqual(len(app.exception), 0)
        return app

    def test_start_without_file(self):
        app = AppTest.from_file(str(APP_PATH)).run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn("Ladda upp", app.info[0].value)

    def test_upload_and_preview(self):
        app = self.run_upload(SAMPLE)
        self.assertEqual([metric.value for metric in app.metric], ["12", "4"])
        self.assertEqual(app.dataframe[1].value.shape, (12, 4))
        self.assertEqual(len(app.get("plotly_chart")), 2)

    def test_sample_selection_and_empty_selection(self):
        app = AppTest.from_file(str(APP_PATH), default_timeout=20).run()
        app.checkbox[0].check().run()
        self.assertEqual(len(app.exception), 0)
        app.multiselect[0].set_value(["antal"]).run()
        self.assertEqual(app.dataframe[1].value.columns.tolist(), ["antal"])
        self.assertEqual(app.selectbox[2].value, "antal")
        self.assertEqual(len(app.get("plotly_chart")), 2)
        app.multiselect[0].set_value([]).run()
        self.assertEqual(len(app.get("plotly_chart")), 0)
        self.assertEqual(len(app.exception), 0)

    def test_text_only(self):
        app = self.run_upload(b"name,category\na,x\nb,y\n")
        self.assertEqual(len(app.get("plotly_chart")), 0)
        self.assertTrue(any("saknar numeriska" in item.value for item in app.info))

    def test_format_settings_and_file_replacement(self):
        app = self.run_upload("namn;pris\nSkål;12,5\n".encode("utf-8"))
        app.selectbox[0].select("Semikolon (;)").run()
        app.selectbox[1].select(",").run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.dataframe[1].value.loc[0, "pris"], 12.5)
        self.assertEqual(len(app.get("plotly_chart")), 2)
        app.file_uploader[0].set_value(("next.csv", b"label;quantity\nx;7\n", "text/csv")).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.multiselect[0].value, ["label", "quantity"])
        self.assertEqual(app.selectbox[2].value, "quantity")
        app.file_uploader[0].clear().run()
        self.assertEqual(len(app.metric), 0)

    def test_all_missing_numeric(self):
        app = self.run_upload(b"value,label\n,x\n,y\n")
        self.assertEqual(len(app.get("plotly_chart")), 0)
        self.assertIn("saknar ändliga", app.warning[0].value)

    def test_single_numeric_value(self):
        app = self.run_upload(b"value\n3\n")
        self.assertEqual(len(app.get("plotly_chart")), 2)

    def test_user_facing_errors(self):
        for content in (b"", b"a,b\n1,2,3", b"a,b\n"):
            with self.subTest(content=content):
                app = self.run_upload(content)
                self.assertEqual(len(app.error), 1)
                self.assertEqual(len(app.get("plotly_chart")), 0)


if __name__ == "__main__":
    unittest.main()
