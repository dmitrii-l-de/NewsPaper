from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.urls import reverse


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    user_rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def update_rating(self):
        self.user_rating = 0
        for post in Post.objects.filter(author__user=self.user):
            self.user_rating += post.post_rating * 3
            for comment in Comment.objects.filter(post=post):
                self.user_rating += comment.comment_rating
        for comment in Comment.objects.filter(user=self.user):
            self.user_rating += comment.comment_rating
        self.save()

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        return reverse('author_update', args=[str(self.id)])


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategoryUser')

    def __str__(self):
        return f'{self.category_name}'


class CategoryUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    post = 'P'
    news = 'N'
    CHOICES = [
        (news, 'Новости'),
        (post, 'Посты')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор поста')
    choice_field = models.CharField(max_length=1, choices=CHOICES, default=news)
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок поста')
    article = models.TextField(verbose_name='Текст поста')
    post_rating = models.IntegerField(default=0, db_column='post_rating', verbose_name='Рейтинг поста')
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория поста')

    def preview(self):
        return f'{self.article[:124]} ...'

    def like(self, value=1):
        self.post_rating += value
        self.save()

    def dislike(self, value=1):
        self.post_rating -= value
        self.save()

    def __str__(self):
        return f'{self.title.title()}, {self.pub_date}: {self.article}'

    def get_absolut_url(self):
        return reverse('news_search', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField(blank=True)
    date_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0, db_column='comment_rating')

    def like(self, value=1):
        self.comment_rating += value
        self.save()

    def dislike(self, value=1):
        self.comment_rating -= value
        self.save()
