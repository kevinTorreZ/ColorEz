# Generated by Django 3.2.16 on 2022-12-13 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Principal', '0010_alter_suscripcion_fecha_termino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suscripcion',
            name='Fecha_termino',
            field=models.DateTimeField(default='0000-00-00', null=True),
        ),
    ]
