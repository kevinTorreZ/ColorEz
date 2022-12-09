# Generated by Django 3.2.16 on 2022-12-09 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metodo_pago',
            fields=[
                ('idMetodo_pago', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('idPlan', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('idProyecto', models.AutoField(primary_key=True, serialize=False)),
                ('Titulo', models.CharField(max_length=25)),
                ('Descripcion', models.TextField()),
                ('Fecha_creacion', models.DateField(verbose_name='')),
                ('photo', models.ImageField(default='/home/coloreze/public_html/static/img/default_image_project.png', upload_to='home/coloreze/public_html/static/img/', verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='')),
                ('username', models.CharField(max_length=24, unique=True, verbose_name='')),
                ('photo', models.ImageField(default=None, max_length=24, upload_to='', verbose_name='')),
                ('activo', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Usuarios_proyecto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Principal.proyecto')),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('idSuscripcion', models.AutoField(primary_key=True, serialize=False)),
                ('Fecha_inicio', models.DateTimeField()),
                ('Fecha_termino', models.DateTimeField()),
                ('Plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Principal.proyecto')),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='proyecto',
            name='Usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=''),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('idFile', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=25)),
                ('Last_modified', models.DateField()),
                ('url', models.FileField(upload_to='')),
                ('Proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Principal.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Comprobante',
            fields=[
                ('idComprobante', models.AutoField(primary_key=True, serialize=False)),
                ('Fecha_pago', models.DateField()),
                ('Costo', models.IntegerField()),
                ('Metodo_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Principal.metodo_pago')),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
