# Generated by Django 3.2.4 on 2021-08-25 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_book_book_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_thumbnail',
            field=models.ImageField(default='no thumbnail', upload_to=''),
            preserve_default=False,
        ),
    ]
