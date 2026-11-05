"""
Unit tests for Publication Year Range Filtering
"""

import unittest
from backend.pubmed import matches_year_range, PaperMetadata, PubMedRetriever


class TestYearFiltering(unittest.TestCase):
    def test_matches_year_range_exact(self):
        self.assertTrue(matches_year_range("2021", 2020, 2026))
        self.assertTrue(matches_year_range("2020", 2020, 2026))
        self.assertTrue(matches_year_range("2026", 2020, 2026))

        self.assertFalse(matches_year_range("2019", 2020, 2026))
        self.assertFalse(matches_year_range("2027", 2020, 2026))
        self.assertFalse(matches_year_range("1995", 2010, 2020))

    def test_matches_year_range_boundary_and_historical(self):
        self.assertTrue(matches_year_range("1998", 1900, 2000))
        self.assertTrue(matches_year_range("1900", 1900, 2000))
        self.assertFalse(matches_year_range("2005", 1900, 2000))

    def test_matches_year_range_with_medline_date_text(self):
        self.assertTrue(matches_year_range("2015 Nov-Dec", 2010, 2020))
        self.assertFalse(matches_year_range("2008 Autumn", 2010, 2020))

    def test_matches_year_range_none_filters(self):
        # When no filters specified, any year passes
        self.assertTrue(matches_year_range("2024", None, None))
        self.assertTrue(matches_year_range("Unknown", None, None))

    def test_fetch_details_filters_by_year(self):
        retriever = PubMedRetriever()
        sample_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <PubmedArticleSet>
          <PubmedArticle>
            <MedlineCitation><PMID>11111</PMID>
              <Article><ArticleTitle>Older Study</ArticleTitle>
                <Journal><JournalIssue><PubDate><Year>1995</Year></PubDate></JournalIssue></Journal>
              </Article>
            </MedlineCitation>
          </PubmedArticle>
          <PubmedArticle>
            <MedlineCitation><PMID>22222</PMID>
              <Article><ArticleTitle>Recent Study</ArticleTitle>
                <Journal><JournalIssue><PubDate><Year>2022</Year></PubDate></JournalIssue></Journal>
              </Article>
            </MedlineCitation>
          </PubmedArticle>
        </PubmedArticleSet>
        """
        all_papers = retriever.parse_xml(sample_xml)
        self.assertEqual(len(all_papers), 2)

        # Filter strictly for 2020-2026
        recent = [p for p in all_papers if matches_year_range(p.year, 2020, 2026)]
        self.assertEqual(len(recent), 1)
        self.assertEqual(recent[0].pmid, "22222")
        self.assertEqual(recent[0].year, "2022")

        # Filter strictly for 1990-2000
        older = [p for p in all_papers if matches_year_range(p.year, 1990, 2000)]
        self.assertEqual(len(older), 1)
        self.assertEqual(older[0].pmid, "11111")
        self.assertEqual(older[0].year, "1995")


if __name__ == "__main__":
    unittest.main()

