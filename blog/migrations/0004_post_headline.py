# Generated by Django 2.2.10 on 2020-03-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='headline',
            field=models.CharField(default='Plain headline for a plain post', max_length=200),
        ),
    ]
