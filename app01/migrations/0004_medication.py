# Generated by Django 3.2 on 2024-05-01 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_repairorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='药品名称')),
                ('reminder_time', models.TimeField(verbose_name='提醒时间')),
                ('image', models.ImageField(blank=True, null=True, upload_to='medications/', verbose_name='药品图片')),
            ],
            options={
                'verbose_name': '用药提醒',
                'verbose_name_plural': '用药提醒',
                'db_table': 'medication',
            },
        ),
    ]
