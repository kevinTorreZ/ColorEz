# Generated by Django 3.2.16 on 2022-12-09 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Principal', '0003_alter_proyecto_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='photo',
            field=models.ImageField(default='media/default_image_project.png', help_text=None, upload_to='media'),
        ),
    ]