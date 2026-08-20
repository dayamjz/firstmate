#!/usr/bin/env python3
"""Tests for predict.py. Run: python3 -m unittest discover dogs (or python3 dogs/test_predict.py)."""

import unittest
from fractions import Fraction

import predict


class TestOwnPhenotypes(unittest.TestCase):
    def test_lola_is_solid_blue(self):
        dog = predict.load_dog("lola")
        desc = predict.describe_dog(dog)
        self.assertIn("solid blue", desc)

    def test_rexy_is_sable_merle_carrier(self):
        dog = predict.load_dog("rexy")
        desc = predict.describe_dog(dog)
        self.assertIn("sable/fawn", desc)
        self.assertIn("merle", desc)

    def test_tilly_is_blue_and_tan(self):
        dog = predict.load_dog("tilly")
        desc = predict.describe_dog(dog)
        self.assertIn("blue and tan", desc)


class TestCross(unittest.TestCase):
    def test_probabilities_sum_to_one(self):
        for pair in [("lola", "rexy"), ("lola", "tilly"), ("rexy", "tilly")]:
            dam, sire = (predict.load_dog(n) for n in pair)
            results, _ = predict.cross(dam, sire)
            self.assertEqual(sum(results.values()), Fraction(1), pair)

    def test_lola_rexy_ee_fraction(self):
        # Ee x Ee -> 25% ee (cream/red) puppies.
        dam, sire = predict.load_dog("lola"), predict.load_dog("rexy")
        results, _ = predict.cross(dam, sire)
        ee_total = sum(p for color, p in results.items() if color.startswith("cream/red"))
        self.assertEqual(ee_total, Fraction(1, 4))

    def test_merle_x_merle_warning(self):
        dam, sire = predict.load_dog("rexy"), predict.load_dog("tilly")
        warns = predict.warnings_for(dam, sire)
        self.assertTrue(any("double merle" in w for w in warns))
        results, notes = predict.cross(dam, sire)
        dm = sum(p for color, p in results.items() if "DOUBLE MERLE" in color)
        self.assertEqual(dm, Fraction(1, 4))

    def test_no_merle_from_lola_rexy_exceeds_half(self):
        # Lola mm x Rexy Mm -> 50% single merle, never double.
        dam, sire = predict.load_dog("lola"), predict.load_dog("rexy")
        results, _ = predict.cross(dam, sire)
        self.assertEqual(sum(p for c, p in results.items() if "DOUBLE MERLE" in c), 0)
        merle = sum(p for c, p in results.items() if "merle" in c and "hidden" not in c)
        self.assertGreater(merle, 0)


class TestPhenotypeRules(unittest.TestCase):
    def test_ee_masks_dominant_black(self):
        g = {
            "E": ("e", "e"), "K": ("KB", "ky"), "A": ("ay", "at"),
            "B": ("B", "B"), "D": ("D", "D"), "Cocoa": ("N", "N"),
            "SaddleTan": ("N", "N"), "S": ("S", "S"), "M": ("m", "m"), "H": ("h", "h"),
        }
        color, _ = predict.phenotype(g)
        self.assertIn("cream/red", color)

    def test_bb_dd_is_lilac(self):
        g = {
            "E": ("E", "E"), "K": ("KB", "ky"), "A": ("ay", "at"),
            "B": ("b", "b"), "D": ("d", "d"), "Cocoa": ("N", "N"),
            "SaddleTan": ("N", "N"), "S": ("S", "S"), "M": ("m", "m"), "H": ("h", "h"),
        }
        color, _ = predict.phenotype(g)
        self.assertEqual(color, "solid lilac")


if __name__ == "__main__":
    unittest.main()
