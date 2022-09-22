from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

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
        return f'{self.user.username}'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    post = 'P'
    news = 'N'
    CHOICES = [
        (news, 'Новости'),
        (post, 'Посты')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice_field = models.CharField(max_length=1, choices=CHOICES, default=news)
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    article = models.TextField()
    post_rating = models.IntegerField(default=0, db_column='post_rating')
    category = models.ManyToManyField(Category, through='PostCategory')

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
