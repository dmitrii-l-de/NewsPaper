from urllib import request

from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Post, PostCategory, User, CategoryUser


@receiver(post_init, sender=PostCategory)
def save_new_post(sender, instance, *args, **kwargs):
   post = instance
   print('TEST')
   print(f'Это айди категории созданного поста {instance.category_id}')
   print(f'Это айди поста {instance.post_id}')
   send_post = Post.objects.filter(id=instance.post_id).values('title')[0]['title']
   send_text = Post.objects.filter(id=instance.post_id).values('article')[0]['article']
   send_url = Post.objects.filter(id=instance.post_id)[0].get_absolut_url()
   print(f'ссылка на пост {send_url}')
   list_user = User.objects.all()
   list_category_user = CategoryUser.objects.all()
   print(f'Список всех юзеров{list_user}')
   print(f'Количество всех юзеров{len(list_user)}')
   add_post_cat = post.category_id
   for user in list_user:
       for category in list_category_user:
           #print(f'Список модели КатегориЮзер {category.category_id}, {category.user_id}')
           if user.id == category.user_id:
               if add_post_cat == category.category_id:
                   print(f'Почты юзеров для отправки : {user.email}')
                   send_post = str(send_post)
                   send_post_id = int(instance.post_id)
                   send_text = str(send_text[:30])

                   print(send_post, send_text)
                   # send_mail(
                   #     f'Письмо для пользователя: {user.first_name}',
                   #     f'Вышел новый пост по вашей категории: {send_post}, {send_text}\n '
                   #     f'Переходите по ссылке чтобы читать больше: {send_url}',
                   #     'gbicfo@yandex.ru',
                   #     ['dmitriy_l2019@list.ru', user.email],
                   #     fail_silently=False,
                   # )

                   html = render_to_string(
                       # передаем в шаблон переменные
                       'mail_to_subscriber.html', {'post_object': post.category, 'send_post': send_post,
                                                   'send_text': send_text, 'post_id': send_post_id},
                   )

                   msg = EmailMultiAlternatives(
                       subject='Уважаемый {user.first_name} {user.last_name} появилась новая статья!',
                       from_email='gbicfo@yandex.ru',
                       to=['dmitriy_l2019@list.ru', 'dmitriy_leznev@mail.ru'], # отправка необходимым людям
                   )
                   msg.attach_alternative(html, 'text/html')
                   msg.send()
   return redirect('post_list')


