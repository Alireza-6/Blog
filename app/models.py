from django.utils import timezone
from django.urls import reverse
from account.models import User
from django.db import models
from django.utils.html import format_html


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey(
        'self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='children', verbose_name='زیر دست'
    )
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس')
    status = models.BooleanField(default=True, verbose_name='وضعیت')
    position = models.IntegerField(verbose_name='موقعیت')

    class Meta:
        ordering = ['parent__id', 'position']
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
        ('i', 'در حال بررسی'),
        ('b', 'برگشت داده شده'),
    )
    title = models.CharField(max_length=200, verbose_name='عنوان')
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles',
        verbose_name='نویسنده'
    )
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='articles')
    description = models.TextField(verbose_name='محتوا')
    image = models.ImageField(upload_to='images', verbose_name='عکس')
    publish = models.DateTimeField(default=timezone.now, verbose_name='انتشار شده در')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')
    updated = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی')
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("account:home")

    def thumbnail_tag(self):
        return format_html(f"<img width='100px' style='border-radius:5px;' src='{self.image.url}'>")

    thumbnail_tag.short_description = "عکس"

    def category_to_str(self):
        return " , ".join([category.title for category in self.category.active()])

    category_to_str.short_description = 'دسته بندی'

    objects = ArticleManager()
