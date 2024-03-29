# Generated by Django 3.2.6 on 2021-09-02 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_article_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_special',
            field=models.BooleanField(default=False, verbose_name='مقاله ویژه'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('d', 'پیش نویس'), ('p', 'منتشر شده'), ('i', 'در حال بررسی'), ('b', 'برگشت داده شده')], max_length=1, verbose_name='وضعیت'),
        ),
    ]
