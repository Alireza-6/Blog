from django.contrib import admin
from .models import Article, Category


# Register your models here.

def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status="p")
    if rows_updated == 1:
        message = 'منتشر شد'
    else:
        message = "منتسر شدند"
    modeladmin.message_user(request, f"{rows_updated} مقاله {message}")


make_published.short_description = "انتشار مقالالت انتخاب شده"


def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status="d")
    if rows_updated == 1:
        message = 'پیش نویس شد'
    else:
        message = "پیش نویس شدند"
    modeladmin.message_user(request, f"{rows_updated} مقاله {message}")


make_draft.short_description = "پیش نویس شدن مقالالت انتخاب شده"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'thumbnail_tag', 'author', 'is_special', 'status', 'category_to_str']
    list_filter = ['author']
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_published, make_draft]


admin.site.register(Article, ArticleAdmin)


def make_active(modeladmin, request, queryset):
    rows_updated = queryset.update(status=True)
    if rows_updated == 1:
        message = 'فعال شد'
    else:
        message = "فعال شدند"
    modeladmin.message_user(request, f"{rows_updated} دسته بندی {message}")


make_active.short_description = "فعال شدن دسته بندی های انتخاب شده"


def deactivate(modeladmin, request, queryset):
    rows_updated = queryset.update(status=False)
    if rows_updated == 1:
        message = 'غیر فعال شد'
    else:
        message = "غیر فعال شدند"
    modeladmin.message_user(request, f"{rows_updated} دسته بندی {message}")


deactivate.short_description = "غیر فعال شدن دسته بندی های انتخاب شده"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['position', 'title', 'parent', 'status']
    list_display_links = ['title']
    list_editable = ['position']
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_active, deactivate]


admin.site.register(Category, CategoryAdmin)
