from django.test import TestCase


class StyleGuideTestCase(TestCase):
    """Tests for the style_guide app frontend."""

    def test_style_guide_frontend_returns_200(self):
        """Test that the style guide page returns 200 OK."""
        response = self.client.get("/style-guide/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Style Guide")
        self.assertTemplateUsed(response, "style_guide/style_guide.html")
