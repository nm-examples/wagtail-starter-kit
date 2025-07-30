from django.db import models
from django.db.models import Max
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page

from app.portfolio.blocks import PortfolioStreamBlock


class PortfolioPage(Page):
    parent_page_types = ["home.HomePage"]

    body = StreamField(
        PortfolioStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Use this section to list your projects and skills.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class OrderableIncrementingModel(Orderable):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            setattr(self, self.sort_order_field, self.get_highest_order() + 1)
        super().save(*args, **kwargs)

    def get_highest_order(self):
        qs = self.__class__.objects.all()
        return (
            qs.aggregate(Max(self.sort_order_field))["%s__max" % self.sort_order_field]
            or 0
        )


class DeveloperSkill(OrderableIncrementingModel):
    name = models.CharField(max_length=255)
    level = models.CharField(
        max_length=50,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
        ],
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("level"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Developer Skill"
        verbose_name_plural = "Developer Skills"
