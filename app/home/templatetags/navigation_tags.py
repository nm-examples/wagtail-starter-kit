from django import template

from app.blog.models import BlogIndexPage

register = template.Library()


@register.simple_tag
def blog_index_page():
    """
    Get the blog index page if it exists.
    """

    return BlogIndexPage.objects.live().first() or None
