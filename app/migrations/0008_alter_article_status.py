# Generated by Django 3.2.6 on 2021-08-31 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_article_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('d', 'پیش نویس'), ('p', 'منتشر شده')], max_length=1, verbose_name='وضعیت'),
        ),
    ]
