# Generated by Django 4.2.6 on 2023-11-15 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0011_knowledgepoints_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledgepoints',
            name='science_education_edition',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='教科版小节'),
        ),
    ]
