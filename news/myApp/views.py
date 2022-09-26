from django.contrib.auth import login
from django.views.generic import (ListView, DetailView,
                                  CreateView, DeleteView, UpdateView)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm, AuthorForm


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    queryset = Post.objects.order_by('-pub_date')
    #ordering = 'pub_date' сортировка по дате публикации
    # также можно использовать сортировку queryset чтобы вывод был по условию:
    # queryset = Post.objects.filter(price__lt = 300).order_by('name') или
    # queryset = Post.objects.order_by('-name') в обратном направлении
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post'


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class NewsSearch(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'search.html'
    context_object_name = 'newssearch'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = ('myApp.add_post',)
    template_name = 'news_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice_field = 'news'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = ('myApp.add_post',)
    template_name = 'articles_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice_field = 'post'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    permission_required = ('myApp.delete_post',)
    success_url = reverse_lazy('post_list')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = ('myApp.change_post',)
    template_name = 'news_edit.html'
    success_url = reverse_lazy('post_list')


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    form_class = AuthorForm
    model = Author
    template_name = 'author_edit.html'
    success_url = reverse_lazy('post_list')

