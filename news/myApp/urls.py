from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, NewsSearch, NewsCreate,
                    ArticlesCreate, PostDelete, PostUpdate, AuthorUpdate
                    )
urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем постам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
    path('', PostList.as_view(), name='post_list'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticlesCreate.as_view(), name='article_create'),
    path('delete/<int:pk>/', PostDelete.as_view(), name='news_delete'),
    path('edit/<int:pk>/', PostUpdate.as_view(), name='news_update'),
    path('author_edit/<int:pk>/', AuthorUpdate.as_view(), name='author_update'),
]
