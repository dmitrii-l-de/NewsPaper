# Generated by Django 4.1.1 on 2022-09-27 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0004_rename_cat_category_categoryuser_id_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoryuser',
            old_name='id_category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='categoryuser',
            old_name='id_user',
            new_name='user',
        ),
    ]