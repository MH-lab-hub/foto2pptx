"""
tests/test_converter.py
=======================
Einfache Tests fuer die Konvertierungsfunktionen.
Ausfuehren mit: python -m unittest discover tests/
              oder: pytest tests/   (wenn pytest installiert)
"""

import unittest
import pandas as pd

from foto2pptx.converter import color_to_rgb, normalize_shape_type, add_emu_columns


class TestColorToRgb(unittest.TestCase):
    def test_bekannte_farbe(self):
        self.assertEqual(color_to_rgb("blau"), (0, 0, 255))

    def test_hex_mit_raute(self):
        self.assertEqual(color_to_rgb("#ff0000"), (255, 0, 0))

    def test_hex_ohne_raute(self):
        self.assertEqual(color_to_rgb("00ff00"), (0, 255, 0))

    def test_unbekannte_farbe(self):
        self.assertEqual(color_to_rgb("xyzunbekannt"), (128, 128, 128))

    def test_leer(self):
        self.assertEqual(color_to_rgb(""), (128, 128, 128))

    def test_nan(self):
        self.assertEqual(color_to_rgb(float("nan")), (128, 128, 128))


class TestNormalizeShapeType(unittest.TestCase):
    def test_kreis(self):
        self.assertEqual(normalize_shape_type("Kreis"), "Kreis")

    def test_circle(self):
        self.assertEqual(normalize_shape_type("circle"), "Kreis")

    def test_rechteck(self):
        self.assertEqual(normalize_shape_type("Rechteck"), "Rechteck")

    def test_andere(self):
        self.assertEqual(normalize_shape_type("Dreieck"), "Rechteck")

    def test_nan(self):
        self.assertEqual(normalize_shape_type(float("nan")), "Rechteck")


class TestAddEmuColumns(unittest.TestCase):
    def test_emu_konvertierung(self):
        df = pd.DataFrame({"x": ["100"], "y": ["200"], "breite": ["300"], "hoehe": ["150"]})
        result = add_emu_columns(df)
        self.assertIn("x_emu", result.columns)
        self.assertEqual(result["x_emu"].iloc[0], 100 * 9525)

    def test_fehlende_spalten(self):
        df = pd.DataFrame({"x": ["50"]})
        result = add_emu_columns(df)
        self.assertIn("x_emu", result.columns)
        self.assertNotIn("y_emu", result.columns)


if __name__ == "__main__":
    unittest.main()
