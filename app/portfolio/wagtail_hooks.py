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
        if request.method == "POST":
            # Handle the AJAX save request
            import json

            from django.http import JsonResponse

            try:
                data = json.loads(request.body)
                order_data = data.get("order", [])

                for item in order_data:
                    skill = DeveloperSkill.objects.get(id=item["id"])
                    skill.sort_order = item["sort_order"]
                    skill.save()

                return JsonResponse({"success": True})
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})

        # GET request - display the reorder page
        skills = DeveloperSkill.objects.all().order_by("sort_order")
        context = {
            "object_list": skills,
        }
        return render(request, "portfolio/snippets/reorder.html", context)


register_snippet(DeveloperSkillViewSet)
