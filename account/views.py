from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin, AuthorsAccessMixin, SuperUserAccessMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.models import Article
from .models import User
from .froms import ProfileForm
from django.contrib.auth.views import LoginView


# Create your views here.


# @login_required(login_url='account:login')
# def home(request):
#     return render(request, 'registration/home.html', {})


class ArticleList(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, FieldsMixin, FormValidMixin, CreateView):
    template_name = 'registration/article_create_update.html'
    model = Article


class ArticleUpdate(LoginRequiredMixin, AuthorAccessMixin, FieldsMixin, FormValidMixin, UpdateView):
    template_name = 'registration/article_create_update.html'
    model = Article


class ArticleDelete(DeleteView, SuperUserAccessMixin):
    model = Article
    template_name = 'registration/article_confirm_delete.html'
    success_url = reverse_lazy('account:home')


class Profile(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile.html'
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwarg = super(Profile, self).get_form_kwargs()
        kwarg.update({
            'user': self.request.user
        })
        return kwarg


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')
