# Generated by Django 3.2 on 2024-05-02 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_alter_medication_reminder_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='username',
            field=models.TextField(default='无效'),
        ),
    ]
