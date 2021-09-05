from account.models import User
from django.shortcuts import render, get_object_or_404
from app.models import Article, Category
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from account.mixins import AuthorAccessMixin


# Create your views here.

class ArticleList(ListView):
    template_name = 'blog/home_list.html'
    queryset = Article.objects.published()
    paginate_by = 2


# def home_page(request, page=1):
#     articles = Article.objects.published()
#     paginator = Paginator(articles, 2)
#     articles = paginator.get_page(page)
#     context = {
#         'articles': articles,
#     }
#     return render(request, 'blog/home_list.html', context)


class ArticleDetail(DetailView):
    template_name = 'blog/article_detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article, slug=slug, status="p")


class ArticlePreview(AuthorAccessMixin, DetailView):
    template_name = 'blog/article_detail.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


# def detail(request, slug):
#     article = get_object_or_404(Article, slug=slug, status="p")
#     context = {
#         'article': article,
#     }
#     return render(request, 'blog/article_detail.html', context)


class CategoryList(ListView):
    template_name = 'blog/category_list.html'
    paginate_by = 2

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     articles = category.articles.published()
#     paginator = Paginator(articles, 2)
#     articles = paginator.get_page(page)
#     context = {
#         'category': category,
#         'articles': articles
#     }
#     return render(request, 'blog/category_list.html', context)


class AuthorList(ListView):
    paginate_by = 2
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
