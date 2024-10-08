# Generated by Django 5.1.1 on 2024-09-09 15:06

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_subject_remove_question_date_created_and_more'),
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subject.subject'),
        ),
        migrations.AddField(
            model_name='question',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
