# Generated by Django 4.2.6 on 2023-11-12 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0010_selections_fill_topic_type_alter_selections_judge'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledgepoints',
            name='type',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='知识点分类'),
        ),
    ]
