# Generated by Django 5.1.1 on 2024-09-10 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0011_question_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='created_at',
        ),
    ]
