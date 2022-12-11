# Generated by Django 3.2.16 on 2022-12-10 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Principal', '0004_alter_proyecto_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='photo',
            field=models.ImageField(default='/media/default_image_project.png', help_text=None, upload_to='media'),
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('idToken', models.AutoField(primary_key=True, serialize=False)),
                ('Token', models.CharField(max_length=50)),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]