# Generated by Django 4.2.6 on 2023-10-27 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterApp', '0003_meep'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
