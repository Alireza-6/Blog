from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from app.models import Article


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['title', 'author', 'slug', 'category', 'description', 'image', 'publish', 'is_special',
                           'status']
        elif request.user.is_author:
            self.fields = ['title', 'slug', 'category', 'description', 'image', 'is_special', 'publish']
        else:
            raise Http404('You cant access this page')
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.status in ['d', 'b'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('You cant access this page')


class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("account:profile")


class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('You cant access this page')
