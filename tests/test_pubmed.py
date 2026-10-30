"""
Unit Tests for PubMed Module (backend/pubmed.py)
"""

import unittest
from backend.pubmed import PaperMetadata, parse_pubmed_xml, NO_ABSTRACT_TEXT, PubMedRetriever

SAMPLE_PUBMED_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation Status="MEDLINE" Owner="NLM">
      <PMID Version="1">23775705</PMID>
      <Article PubModel="Print-Electronic">
        <Journal>
          <Title>The Cochrane database of systematic reviews</Title>
          <JournalIssue>
            <PubDate>
              <Year>2013</Year>
            </PubDate>
          </JournalIssue>
        </Journal>
        <ArticleTitle>Zinc for the common cold.</ArticleTitle>
        <Abstract>
          <AbstractText Label="BACKGROUND">The common cold is widespread.</AbstractText>
          <AbstractText Label="RESULTS">Zinc reduces duration of cold symptoms.</AbstractText>
        </Abstract>
        <AuthorList>
          <Author>
            <LastName>Singh</LastName>
            <ForeName>Meenu</ForeName>
          </Author>
        </AuthorList>
      </Article>
    </MedlineCitation>
    <PubmedData>
      <ArticleIdList>
        <ArticleId IdType="pubmed">23775705</ArticleId>
        <ArticleId IdType="doi">10.1002/14651858.CD001364.pub4</ArticleId>
      </ArticleIdList>
    </PubmedData>
  </PubmedArticle>
  <PubmedArticle>
    <MedlineCitation Status="MEDLINE" Owner="NLM">
      <PMID Version="1">99999999</PMID>
      <Article PubModel="Print">
        <Journal>
          <Title>Brief Communications</Title>
        </Journal>
        <ArticleTitle>Editorial Note on Immunity</ArticleTitle>
        <AuthorList>
          <Author>
            <LastName>Doe</LastName>
            <ForeName>John</ForeName>
          </Author>
        </AuthorList>
      </Article>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>
"""


class TestPubMed(unittest.TestCase):
    def test_paper_metadata_url(self):
        paper = PaperMetadata(pmid="23775705", title="Zinc Study", abstract="Abstract text")
        self.assertEqual(paper.url, "https://pubmed.ncbi.nlm.nih.gov/23775705/")
        self.assertTrue(paper.has_abstract)

    def test_parse_pubmed_xml_with_abstract(self):
        papers = parse_pubmed_xml(SAMPLE_PUBMED_XML)
        self.assertEqual(len(papers), 2)
        
        # Paper 1: has abstract
        p1 = papers[0]
        self.assertEqual(p1.pmid, "23775705")
        self.assertEqual(p1.title, "Zinc for the common cold")  # Trailing period stripped
        self.assertEqual(p1.year, "2013")
        self.assertEqual(p1.authors, ["Meenu Singh"])
        self.assertEqual(p1.doi, "10.1002/14651858.CD001364.pub4")
        self.assertTrue(p1.has_abstract)
        self.assertIn("Background: The common cold", p1.abstract)
        self.assertIn("Results: Zinc reduces duration", p1.abstract)

    def test_parse_pubmed_xml_missing_abstract(self):
        papers = parse_pubmed_xml(SAMPLE_PUBMED_XML)
        # Paper 2: missing abstract
        p2 = papers[1]
        self.assertEqual(p2.pmid, "99999999")
        self.assertFalse(p2.has_abstract)
        self.assertEqual(p2.abstract, NO_ABSTRACT_TEXT)

    def test_empty_xml(self):
        papers = parse_pubmed_xml(b"<EmptySet></EmptySet>")
        self.assertEqual(papers, [])


if __name__ == "__main__":
    unittest.main()
