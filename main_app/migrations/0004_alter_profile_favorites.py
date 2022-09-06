# Generated by Django 4.0.6 on 2022-09-06 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favorites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favorite', to='main_app.recipe'),
        ),
    ]
