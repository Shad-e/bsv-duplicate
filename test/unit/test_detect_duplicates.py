import pytest
from src.util.detector import detect_duplicates

@pytest.mark.unit
@pytest.mark.parametrize(
    "desc,entries,expected_count,raises",
    [
        # TC1: 0 articles
        ("no articles", "", 0, ValueError),
        # TC2: 1 article
        ("one article", "@article{A,\n  doi={10.1},\n}\n", 0, ValueError),
        # TC3: 2 articles, same key, same doi
        (
            "2 articles, same key, same doi",
            "@article{A,\n  doi={10.1},\n}\n@article{A,\n  doi={10.1},\n}\n",
            1,
            None,
        ),
        # TC4: 2 articles, same key, different doi
        (
            "2 articles, same key, different doi",
            "@article{A,\n  doi={10.1},\n}\n@article{A,\n  doi={10.2},\n}\n",
            0,
            None,
        ),
        # TC5: 2 articles, different key, same doi
        (
            "2 articles, different key, same doi",
            "@article{A,\n  doi={10.1},\n}\n@article{B,\n  doi={10.1},\n}\n",
            0,
            None,
        ),
        # TC6: 2 articles, same key, one missing doi
        (
            "2 articles, same key, one missing doi",
            "@article{A,\n  doi={10.1},\n}\n@article{A,\n}\n",
            1,
            None,
        ),
        # TC7: 2 articles, same key, both missing doi
        (
            "2 articles, same key, both missing doi",
            "@article{A,\n}\n@article{A,\n}\n",
            1,
            None,
        ),
        # TC8: 2 articles, different key, one missing doi
        (
            "2 articles, different key, one missing doi",
            "@article{A,\n  doi={10.1},\n}\n@article{B,\n}\n",
            0,
            None,
        ),
        # TC9: 2 articles, different key, both missing doi
        (
            "2 articles, different key, both missing doi",
            "@article{A,\n}\n@article{B,\n}\n",
            0,
            None,
        ),
        # TC10: 3 articles, two are duplicates
        (
            "3 articles, two are duplicates",
            "@article{A,\n  doi={10.1},\n}\n@article{A,\n  doi={10.1},\n}\n@article{B,\n  doi={10.2},\n}\n",
            1,
            None,
        ),
    ]
)
def test_detect_duplicates(desc, entries, expected_count, raises):
    if raises:
        with pytest.raises(raises):
            detect_duplicates(entries)
    else:
        duplicates = detect_duplicates(entries)
        assert len(duplicates) == expected_count, f"{desc}: Expected {expected_count} duplicates, got {len(duplicates)}"

# ---------------------------------------------------------------
# Test structure and independence

# Test cases are parameterized with a description, BibTeX string, expected duplicate count, and expected exception.
# Each test is independent and does not share state.
# Pytest runs each case separately.
# The main challenge was keeping the BibTeX strings minimal but valid for the parser.