# Generated by Django 4.0.6 on 2022-08-31 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.CharField(default='recipe description', max_length=255),
            preserve_default=False,
        ),
    ]
