# Generated by Django 4.2.7 on 2023-11-02 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('nacionalidad', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('website', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('año_de_publicacion', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('hojas', models.IntegerField()),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.autor')),
                ('editorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.editorial')),
            ],
        ),
    ]
