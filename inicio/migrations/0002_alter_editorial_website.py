# Generated by Django 4.2.7 on 2023-11-02 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editorial',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]