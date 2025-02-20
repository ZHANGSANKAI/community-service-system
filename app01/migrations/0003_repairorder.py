# Generated by Django 3.2 on 2024-05-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20240429_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepairOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('phone_number', models.CharField(max_length=11, verbose_name='电话号码')),
                ('address', models.TextField(verbose_name='地址')),
                ('description_audio', models.FileField(upload_to='descriptions/')),
            ],
            options={
                'verbose_name': '维修订单',
                'verbose_name_plural': '维修订单',
                'db_table': 'repairorder',
            },
        ),
    ]
