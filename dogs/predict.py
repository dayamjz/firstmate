#!/usr/bin/env python3
"""Predict possible coat colors of puppies from two parents' DNA reports.

Dog genotypes live in dogs/<name>.json (captured from Embark coat color
panels). Usage:

    python3 predict.py list                 # show each dog and her own expected color
    python3 predict.py show <dog>           # one dog's genotype and expected color
    python3 predict.py cross <dam> <sire>   # puppy color probabilities for a pairing

Only standard-library Python. See README.md for the genetics model and its
limits (intensity shade and white spotting amount are only approximated).
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

DOGS_DIR = Path(__file__).parent / "dogs"

# Dominance order within each locus, most dominant first. Genotypes are
# normalized to this order so "Ee" and "eE" are the same genotype.
DOMINANCE = {
    "E": ["Em", "Eg", "E", "e"],
    "K": ["KB", "kbr", "ky"],
    "A": ["ay", "aw", "at", "a"],
    "B": ["B", "b"],
    "D": ["D", "d"],
    "Cocoa": ["N", "co"],
    "SaddleTan": ["I", "N"],
    "S": ["S", "sp"],
    "M": ["M", "m"],
    "H": ["H", "h"],
}

CROSSED_LOCI = list(DOMINANCE)


def load_dog(name: str) -> dict:
    path = DOGS_DIR / f"{name.lower()}.json"
    if not path.exists():
        available = ", ".join(sorted(p.stem for p in DOGS_DIR.glob("*.json") if p.stem != "sire-template"))
        raise SystemExit(f"No DNA record for '{name}'. Available dogs: {available}")
    dog = json.loads(path.read_text())
    for locus, alleles in dog["coat_color_loci"].items():
        if locus not in DOMINANCE:
            raise SystemExit(f"{dog['name']}: unknown locus '{locus}'")
        for allele in alleles:
            if allele not in DOMINANCE[locus]:
                raise SystemExit(f"{dog['name']}: unknown allele '{allele}' at locus {locus}")
        if len(alleles) != 2:
            raise SystemExit(f"{dog['name']}: locus {locus} must list exactly two alleles")
    return dog


def normalize(locus: str, pair: tuple[str, str]) -> tuple[str, str]:
    order = DOMINANCE[locus]
    return tuple(sorted(pair, key=order.index))


def offspring_locus_distribution(locus: str, dam: dict, sire: dict) -> dict[tuple[str, str], Fraction]:
    """Punnett square for one locus: each parent passes either allele with p=1/2."""
    dist: dict[tuple[str, str], Fraction] = defaultdict(Fraction)
    for a in dam["coat_color_loci"][locus]:
        for b in sire["coat_color_loci"][locus]:
            dist[normalize(locus, (a, b))] += Fraction(1, 4)
    return dict(dist)


def has(genotype: tuple[str, str], allele: str) -> bool:
    return allele in genotype


def count(genotype: tuple[str, str], allele: str) -> int:
    return sum(1 for a in genotype if a == allele)


def eumelanin_color(g: dict[str, tuple[str, str]]) -> str:
    """Color of dark (eumelanin) pigment from B, D, and Cocoa loci."""
    brown = count(g["B"], "b") == 2 or count(g["Cocoa"], "co") == 2
    dilute = count(g["D"], "d") == 2
    if brown and dilute:
        return "lilac"
    if brown:
        return "chocolate"
    if dilute:
        return "blue"
    return "black"


def phenotype(g: dict[str, tuple[str, str]]) -> tuple[str, list[str]]:
    """Map a full genotype to (color description, notes)."""
    notes: list[str] = []
    eum = eumelanin_color(g)
    merle_n = count(g["M"], "M")

    if count(g["E"], "e") == 2:
        # ee: only red pigment shows in the coat; K and A are hidden.
        base = "cream/red (shade set by intensity genes)"
        color = f"{base}, {eum} nose/skin pigment"
        if merle_n >= 1:
            notes.append("merle hidden on cream/red coat (cryptic merle - test before breeding)")
    else:
        if has(g["E"], "Em"):
            notes.append("melanistic mask")
        if has(g["K"], "KB"):
            color = f"solid {eum}"
        elif has(g["K"], "kbr"):
            color = f"{eum} brindle pattern"
        elif has(g["A"], "ay"):
            color = f"sable/fawn with {eum} shading"
        elif has(g["A"], "aw"):
            color = f"wolf sable (agouti) with {eum} banding"
        elif has(g["A"], "at"):
            color = f"{eum} and tan"
            if has(g["SaddleTan"], "I"):
                notes.append("saddle tan pattern possible (RALY)")
        else:
            color = f"recessive solid {eum}"
        if merle_n == 1:
            color += ", merle"

    if merle_n == 2:
        color += " DOUBLE MERLE"
        notes.append("double merle: mostly white, high risk of deafness/blindness")

    if count(g["S"], "sp") == 2:
        notes.append("piebald (significant white spotting)")
    elif has(g["S"], "sp"):
        notes.append("possible small white markings")

    return color, notes


def cross(dam: dict, sire: dict):
    """Enumerate offspring genotype combinations and aggregate by phenotype."""
    per_locus = {locus: offspring_locus_distribution(locus, dam, sire) for locus in CROSSED_LOCI}
    results: dict[str, Fraction] = defaultdict(Fraction)
    note_probs: dict[str, Fraction] = defaultdict(Fraction)
    loci = list(per_locus)
    for combo in itertools.product(*(per_locus[l].items() for l in loci)):
        g = {locus: pair for locus, (pair, _) in zip(loci, combo)}
        p = Fraction(1)
        for _, (_, lp) in zip(loci, combo):
            p *= lp
        color, notes = phenotype(g)
        results[color] += p
        for note in notes:
            note_probs[note] += p
    return dict(results), dict(note_probs)


def warnings_for(dam: dict, sire: dict) -> list[str]:
    warns = []
    if "M" in dam["coat_color_loci"] and "M" in sire["coat_color_loci"]:
        if count(tuple(dam["coat_color_loci"]["M"]), "M") >= 1 and count(tuple(sire["coat_color_loci"]["M"]), "M") >= 1:
            warns.append(
                "BREEDING WARNING: both parents carry merle. 25% of puppies would be "
                "double merle, with high risk of deafness and eye defects. This pairing "
                "is widely considered unethical."
            )
    if dam.get("sex") == sire.get("sex"):
        warns.append(
            f"Note: both dogs are recorded as {dam.get('sex')}s - this is a hypothetical "
            "cross. Add a real sire from dogs/sire-template.json for a plannable litter."
        )
    return warns


def describe_dog(dog: dict) -> str:
    g = {locus: normalize(locus, tuple(alleles)) for locus, alleles in dog["coat_color_loci"].items()}
    color, notes = phenotype(g)
    line = f"{dog['name']} ({dog['breed']}, {dog['sex']}): {color}"
    if notes:
        line += " [" + "; ".join(notes) + "]"
    return line


def fmt_pct(p: Fraction) -> str:
    return f"{float(p) * 100:6.2f}%"


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "list":
        for path in sorted(DOGS_DIR.glob("*.json")):
            if path.stem == "sire-template":
                continue
            print(describe_dog(load_dog(path.stem)))
        return 0

    if len(argv) >= 3 and argv[1] == "show":
        dog = load_dog(argv[2])
        print(describe_dog(dog))
        print(f"  source: {dog['embark_url']} (captured {dog['captured']})")
        for locus, alleles in dog["coat_color_loci"].items():
            print(f"  {locus:10s} {'/'.join(alleles)}")
        if dog.get("intensity"):
            print(f"  {'Intensity':10s} {dog['intensity']} (linkage-based, not crossed)")
        return 0

    if len(argv) >= 4 and argv[1] == "cross":
        dam, sire = load_dog(argv[2]), load_dog(argv[3])
        print(f"Cross: {dam['name']} x {sire['name']}")
        print(f"  {describe_dog(dam)}")
        print(f"  {describe_dog(sire)}")
        print()
        for warn in warnings_for(dam, sire):
            print(f"!! {warn}")
            print()
        results, note_probs = cross(dam, sire)
        print("Puppy coat color probabilities:")
        for color, p in sorted(results.items(), key=lambda kv: -kv[1]):
            print(f"  {fmt_pct(p)}  {color}")
        assert sum(results.values()) == 1
        if note_probs:
            print("\nAdditional pattern/health notes (chance any given puppy is affected):")
            for note, p in sorted(note_probs.items(), key=lambda kv: -kv[1]):
                print(f"  {fmt_pct(p)}  {note}")
        print(
            "\nCaveats: red shade (cream vs orange) depends on intensity genes not "
            "modeled here; amount of white and merle expression vary; spotting/ticking "
            "are not fully testable."
        )
        return 0

    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
