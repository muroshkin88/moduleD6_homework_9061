# Generated by Django 4.1.6 on 2023-06-21 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_rename_postcategory_post_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcategory',
            old_name='categoryThrough',
            new_name='category',
        ),
    ]
