import pytest
from src.util.detector import detect_duplicates
from src.util.parser import Article

def make_bibtex_entry(key, doi=None):
    bib = f"@article{{{key},\n"
    if doi:
        bib += f"  doi={{{doi}}},\n"
    bib += "}\n"
    return bib

@pytest.mark.unit
@pytest.mark.parametrize(
    "desc,entries,expected_count,raises",
    [
        # TC1: 0 articles
        ("no articles", "", 0, ValueError),
        # TC2: 1 article
        ("one article", make_bibtex_entry("A", "10.1"), 0, ValueError),
        # TC3: 2 articles, same key, same doi
        (
            "2 articles, same key, same doi",
            make_bibtex_entry("A", "10.1") + make_bibtex_entry("A", "10.1"),
            1,
            None,
        ),
        # TC4: 2 articles, same key, different doi
        (
            "2 articles, same key, different doi",
            make_bibtex_entry("A", "10.1") + make_bibtex_entry("A", "10.2"),
            0,
            None,
        ),
        # TC5: 2 articles, different key, same doi
        (
            "2 articles, different key, same doi",
            make_bibtex_entry("A", "10.1") + make_bibtex_entry("B", "10.1"),
            0,
            None,
        ),
        # TC6: 2 articles, same key, one missing doi
        (
            "2 articles, same key, one missing doi",
            make_bibtex_entry("A", "10.1") + make_bibtex_entry("A"),
            1,
            None,
        ),
        # TC7: 2 articles, same key, both missing doi
        (
            "2 articles, same key, both missing doi",
            make_bibtex_entry("A") + make_bibtex_entry("A"),
            1,
            None,
        ),
        # TC8: 2 articles, different key, one missing doi
        (
            "2 articles, different key, one missing doi",
            make_bibtex_entry("A", "10.1") + make_bibtex_entry("B"),
            0,
            None,
        ),
        # TC9: 2 articles, different key, both missing doi
        (
            "2 articles, different key, both missing doi",
            make_bibtex_entry("A") + make_bibtex_entry("B"),
            0,
            None,
        ),
        # TC10: 3 articles, two are duplicates
        (
            "3 articles, two are duplicates",
            make_bibtex_entry("A", "10.1") + make_bibtex_entry("A", "10.1") + make_bibtex_entry("B", "10.2"),
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
# Test structure and independence explanation

# How test cases are structured:
# - Each test case is parameterized with a description, BibTeX input, expected duplicate count, and expected exception.
# - The helper function 'make_bibtex_entry' generates minimal BibTeX entries for each scenario.
# - The test covers all relevant combinations from the test table, mapping directly to the logic in detect_duplicates.

# How test independence is ensured:
# - Each test case is self-contained, with its own input data and expected outcome.
# - No test modifies global state or depends on the outcome of another test.
# - Pytest's parameterization ensures each scenario runs in isolation.

# Challenges faced:
# - Ensuring the BibTeX input is minimal yet valid for the parser.
# - Matching the parser's behavior (which only extracts key and doi) with the test data.
# - Verifying the correct number of duplicates, since the function returns only the duplicate articles, not all pairs.