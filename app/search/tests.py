from django.test import TestCase


class SearchTestCase(TestCase):
    """Tests for the search app frontend."""

    def test_search_frontend_returns_200(self):
        """Test that the search page returns 200 OK."""
        response = self.client.get("/search/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search")
        self.assertTemplateUsed(response, "search/search.html")

    def test_search_with_query_returns_200(self):
        """Test that search with a query returns 200 OK."""
        response = self.client.get("/search/?query=test")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/search.html")

    def test_search_no_results(self):
        """Test that search with no results still returns 200 OK."""
        response = self.client.get("/search/?query=empty")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No results found")
        self.assertTemplateUsed(response, "search/search.html")

    def test_search_empty_query(self):
        """Test that search with empty query returns 200 OK."""
        response = self.client.get("/search/?query=")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No results found")
        self.assertTemplateUsed(response, "search/search.html")
