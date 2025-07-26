from django import template

from app.blog.models import BlogIndexPage, BlogTagIndexPage

register = template.Library()


@register.simple_tag
def blog_index_page():
    """
    Get the blog index page if it exists.
    """

    return BlogIndexPage.objects.live().first() or None


@register.simple_tag
def blog_tags_page():
    """
    Get the blog tags page if it exists.
    """

    return BlogTagIndexPage.objects.live().first() or None
