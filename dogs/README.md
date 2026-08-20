# Dogs — DNA reports and puppy color prediction

DNA coat-color reports for the fleet's dogs, captured from their public Embark
profiles, plus a small dependency-free predictor that estimates the coat colors
of potential future puppies from any pairing.

## The dogs

| Dog | Embark profile | Breed | Sex | Own expected color |
|------|----------------|-------|-----|--------------------|
| Lola (Embark name "Ray") | [my.embarkvet.com/dog/ray289](https://my.embarkvet.com/dog/ray289) | Pomeranian 100% | F | solid blue (dilute black) |
| Rexy | [my.embarkvet.com/dog/rexy10](https://my.embarkvet.com/dog/rexy10) | Pomeranian 100% | F | cream sable, single merle |
| Tilly | [my.embarkvet.com/dog/tilly2248](https://my.embarkvet.com/dog/tilly2248) | Pomeranian 100% | F | blue and tan (possible saddle), single merle |

Full genotypes, Embark's own wording, and capture dates live in
[`dogs/`](dogs/) as one JSON file per dog.

## Usage

```sh
python3 predict.py list                 # every dog and her own expected color
python3 predict.py show tilly           # one dog's full genotype
python3 predict.py cross lola rexy      # puppy color probabilities for a pairing
```

All three current dogs are female, so crosses between them are hypothetical
"what would the genetics do" runs. To plan a real litter, copy
[`dogs/sire-template.json`](dogs/sire-template.json) to `dogs/<sire-name>.json`,
fill in the sire's alleles from his DNA report, and cross against him.

Run tests with:

```sh
python3 -m unittest discover -s dogs   # from the repo root
```

## Important breeding note: merle

**Rexy and Tilly each carry one merle allele (M\*m).** Never pair two
merle-carrying dogs: 25% of such a litter would be double merle, with a high
risk of deafness and serious eye defects. The predictor refuses to stay quiet
about this — `cross rexy tilly` prints a prominent warning. When choosing an
outside sire for Rexy or Tilly, pick a non-merle (mm) sire; for Lola (mm) a
merle sire is genetically safe.

Also note Rexy's and Tilly's merle can hide on light coats (cryptic/sable
merle), which is exactly why sire candidates should be DNA-tested rather than
judged by eye.

## How prediction works

For each coat-color locus the puppy inherits one allele from each parent with
equal probability (a Punnett square). The predictor enumerates every genotype
combination across loci, applies standard dominance/epistasis rules, and sums
the probabilities of identical phenotypes:

1. **E locus (MC1R)** — `ee` puppies show only red/cream pigment regardless of
   all other loci (K and A are hidden but still passed on).
2. **K locus (CBD103)** — any `KB` makes the eumelanin coat solid; `kyky` lets
   the A locus pattern show.
3. **A locus (ASIP)** — `ay` sable/fawn > `aw` wolf sable > `at` tan points >
   `a` recessive black.
4. **B and D loci (+ Cocoa)** — set the shade of dark pigment: black; `dd`
   blue; `bb` chocolate; `bb dd` lilac. Applies to coat and to nose/skin of
   red dogs.
5. **M locus (PMEL)** — one `M` = merle pattern; two = double merle (flagged
   as a health risk).
6. **S locus (MITF)** — `spsp` piebald, `Ssp` possible small white marks —
   reported as notes because white amount is poorly predictable.
7. **Saddle tan (RALY)** — noted on tan-pointed puppies carrying `I`.

### Known limits

- **Red shade** (cream vs orange vs red) comes from Embark's linkage-based
  intensity loci, which can't be crossed like simple alleles; each dog's
  intensity class is stored in her JSON and shade is reported as a range.
- **White amount, merle expression, spotting and ticking** vary beyond what DNA
  panels predict; treat the notes as likelihoods, not guarantees.
- Probabilities are per-puppy odds, not guarantees about litter composition.

## Data provenance

Genotypes were read from each dog's public Embark profile pages on
2026-08-20 (the profiles are JavaScript-rendered; they were captured with a
headless browser and transcribed into the JSON files verbatim, including
Embark's own result wording under `embark_reported` for cross-checking).
Re-capture any time the dogs are retested or a new dog joins.
