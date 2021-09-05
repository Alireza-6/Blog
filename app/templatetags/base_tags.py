from django import template

from ..models import Category

register = template.Library()


@register.simple_tag
def title():
    return 'وبلاگ جنگویی'


@register.inclusion_tag('blog/partials/category_navbar.html')
def category_navbar():
    categories = Category.objects.filter(status=True)
    return {
        'categories': categories
    }


@register.inclusion_tag('registration/partials/link.html')
def link(request, link_name, content, classes):
    return {
        'request': request,
        'link_name': link_name,
        'content': content,
        'link': f"account:{link_name}",
        'classes': classes
    }
