# Generated by Django 4.2.7 on 2023-11-18 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0009_resena'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libro',
            old_name='anio_de_publicacion',
            new_name='fecha_de_publicacion',
        ),
    ]