"""The Baitome registry, version 0.1: elements, actions, bonds, compounds.

Everything here is declared structure: 32 candidate appraisal elements in 7
families, an action alphabet of 12, a small set of action-specific bonds,
and 40 named compounds as sparse element formulas with their vernacular
family. The affinity and bond magnitudes are structural calibration, not
fitted data; the paper says so. Where the empirical record anchors a
direction (negativity and clicking, out-group language and sharing, moral
words and diffusion), the sign and rough ordering follow it.
"""
from __future__ import annotations

FAMILIES = {
    "epistemic":  ["IG", "NV", "SU", "AM", "ER"],
    "defensive":  ["TH", "LO", "UC", "DG"],
    "appetitive": ["RW", "SC", "SX", "AS", "PL"],
    "moral":      ["NO", "BL", "IJ", "VE"],
    "identity":   ["IN", "OUT", "BE", "SP", "SS"],
    "relational": ["EM", "RC", "PA", "MM"],
    "status":     ["VA", "CO", "RE", "AU", "CM"],
}
ELEMENTS = [e for fam in FAMILIES.values() for e in fam]
E = {e: i for i, e in enumerate(ELEMENTS)}

ACTIONS = ["Or", "Ck", "Dw", "Rx", "Rp", "Qs", "Sh", "Fo", "Rt", "Cv",
           "Ds", "Mb"]
A = {a: i for i, a in enumerate(ACTIONS)}

# element -> {action: affinity}; scale is arbitrary but shared
AFFINITY = {
    "IG": {"Or": .6, "Ck": 1.0, "Dw": .6},
    "NV": {"Or": .8, "Ck": .6, "Dw": .3},
    "SU": {"Or": 1.0, "Ck": .5, "Sh": .3},
    "AM": {"Ck": .5, "Dw": .4, "Rp": .3},
    "ER": {"Rp": .9, "Qs": .4, "Dw": .3},
    "TH": {"Ck": .5, "Sh": .4, "Rt": .5, "Or": .4},
    "LO": {"Ck": .4, "Cv": .5, "Rt": .4},
    "UC": {"Rt": .7, "Dw": .3},
    "DG": {"Or": .7, "Sh": .4},
    "RW": {"Ck": .5, "Cv": .8, "Rx": .3},
    "SC": {"Ck": .5, "Cv": .7},
    "SX": {"Or": .7, "Ck": .6, "Fo": .5},
    "AS": {"Fo": .6, "Cv": .5, "Sh": .2},
    "PL": {"Dw": .6, "Rx": .5, "Sh": .3},
    "NO": {"Rp": .7, "Sh": .6, "Qs": .5, "Rx": .3},
    "BL": {"Rp": .6, "Qs": .5, "Sh": .3},
    "IJ": {"Sh": .7, "Rp": .4, "Mb": .5},
    "VE": {"Rx": .7, "Sh": .5},
    "IN": {"Sh": .6, "Rx": .5, "Fo": .4},
    "OUT": {"Rp": .6, "Qs": .7, "Sh": .6},
    "BE": {"Rx": .5, "Fo": .5, "Sh": .3},
    "SP": {"Ck": .4, "Fo": .5, "Cv": .4},
    "SS": {"Sh": .6, "Qs": .4, "Rx": .3},
    "EM": {"Rx": .6, "Sh": .5, "Cv": .5},
    "RC": {"Rp": .4, "Cv": .6, "Rx": .3},
    "PA": {"Fo": .8, "Rt": .6, "Cv": .3},
    "MM": {"Rp": .4, "Sh": .5, "Rx": .4},
    "VA": {"Rx": .6, "Fo": .5, "Sh": .3},
    "CO": {"Rp": .7, "Qs": .4, "Dw": .3},
    "RE": {"Rp": .7, "Qs": .5},
    "AU": {"Cv": .6, "Ds": .8, "Ck": .3},
    "CM": {"Rt": .8, "Cv": .5},
}

# bonds: (element, element, action, strength); positive is synergy
BONDS = [
    ("NO", "BL", "Rp", .5), ("NO", "BL", "Sh", .3),
    ("NO", "OUT", "Sh", .6), ("NO", "OUT", "Qs", .5),
    ("IG", "SU", "Or", .4), ("IG", "SU", "Ck", .5),
    ("SC", "LO", "Cv", .6),
    ("ER", "CO", "Rp", .6),
    ("EM", "RC", "Cv", .5), ("EM", "RC", "Sh", .3),
    ("TH", "UC", "Rt", .5), ("TH", "UC", "Sh", -.4),
    ("VA", "IN", "Sh", .4),
    ("AM", "AU", "Ds", -.3),
]

# 40 named compounds: name -> (family, formula)
COMPOUNDS = {
    # acquisition and consumption
    "clickbait":        ("acquisition", ["IG", "SU", "AM"]),
    "watchbait":        ("acquisition", ["IG", "CM"]),
    "thumbnail bait":   ("acquisition", ["SU", "IG", "SX"]),
    "shockbait":        ("acquisition", ["SU", "DG"]),
    "fearbait":         ("acquisition", ["TH", "UC", "LO"]),
    "doombait":         ("acquisition", ["TH", "UC", "LO", "CM"]),
    "mystery bait":     ("acquisition", ["IG", "AM", "SU", "NV"]),
    # conflict and expressive
    "ragebait":         ("conflict", ["NO", "BL", "IJ", "OUT", "RE"]),
    "flamebait":        ("conflict", ["OUT", "RE", "CO", "NO"]),
    "trollbait":        ("conflict", ["RE", "AM", "CO"]),
    "controversy bait": ("conflict", ["AM", "NO", "OUT"]),
    "hot-take bait":    ("conflict", ["NO", "RE", "SS"]),
    "correction bait":  ("conflict", ["ER", "CO", "RE"]),
    "dunk bait":        ("conflict", ["ER", "NO", "OUT", "CO"]),
    "concern bait":     ("conflict", ["EM", "AU", "OUT", "NO"]),
    "provocation bait": ("conflict", ["RE", "NO", "SU"]),
    # identity, affiliation, status
    "tribal bait":      ("identity", ["IN", "OUT", "BE", "SS"]),
    "identity bait":    ("identity", ["IN", "SS", "VA"]),
    "validation bait":  ("identity", ["VA", "IN", "SS", "BE"]),
    "challenge bait":   ("identity", ["CO", "RE", "IG"]),
    "intelligence bait":("identity", ["CO", "VA", "IG"]),
    "purity bait":      ("identity", ["NO", "DG", "IN", "OUT"]),
    "virtue bait":      ("identity", ["VE", "SS", "IN"]),
    "nostalgia bait":   ("identity", ["MM", "BE", "IN"]),
    "thirst bait":      ("identity", ["SX", "AS", "PA"]),
    "aspiration bait":  ("identity", ["AS", "VA", "SP"]),
    # care and relational
    "sympathy bait":    ("care", ["EM", "LO", "RC"]),
    "grief bait":       ("care", ["EM", "LO", "PA", "MM"]),
    "vulnerability bait":("care", ["EM", "VA", "RC"]),
    "parasocial bait":  ("care", ["PA", "RC", "VA", "SC"]),
    "guilt bait":       ("care", ["RC", "NO", "BL"]),
    "rescue bait":      ("care", ["EM", "TH", "RC"]),
    # reward, retention, conversion
    "FOMO bait":        ("retention", ["SC", "LO", "SP", "AS"]),
    "giveaway bait":    ("retention", ["RW", "SC", "SP", "RC"]),
    "streak bait":      ("retention", ["CM", "RW", "LO"]),
    "social-proof bait":("retention", ["SP", "BE", "AS"]),
    "notification bait":("retention", ["IG", "PA", "RW"]),
    # deceptive and extraction
    "phishing bait":    ("extraction", ["AU", "TH", "LO", "SC"]),
    "scam bait":        ("extraction", ["RW", "AU", "SC"]),
    "credential bait":  ("extraction", ["AU", "TH", "UC"]),
}

COMPOUND_FAMILIES = ["acquisition", "conflict", "identity", "care",
                     "retention", "extraction"]
