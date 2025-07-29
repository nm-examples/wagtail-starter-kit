from django.shortcuts import render
from django.urls import path
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from app.portfolio.models import DeveloperSkill


class DeveloperSkillViewSet(SnippetViewSet):
    """ViewSet for managing DeveloperSkill snippets."""

    model = DeveloperSkill
    list_display = ("name", "level", "sort_order")
    search_fields = ("name", "level")
    list_filter = ("level",)
    ordering = ("name",)

    def get_urlpatterns(self):
        return super().get_urlpatterns() + [
            path("reorder/", self.reorder_view, name="reorder"),
        ]

    def reorder_view(self, request):
        return render(request, "portfolio/snippets/reorder.html")


register_snippet(DeveloperSkillViewSet)
