# Generated by Django 4.2.6 on 2023-10-28 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_knowledgepoints_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selections',
            name='judge',
            field=models.BooleanField(default=False, verbose_name='正误'),
        ),
    ]
