# Generated by Django 4.2.7 on 2023-11-10 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0006_alter_libro_portada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='portada',
            field=models.ImageField(null=True, upload_to='imagenes_libros/'),
        ),
    ]