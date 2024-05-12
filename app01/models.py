from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    phonenumber = models.CharField(max_length=11,unique=True,verbose_name="手机号")
    password = models.CharField(max_length=255)
    address = models.TextField()

    class Meta:
        db_table = 'users'
        verbose_name="用户"
        verbose_name_plural=verbose_name


class Food(models.Model):
    name = models.TextField()
    category = models.TextField()
    price = models.TextField()
    sels = models.TextField()
    image = models.ImageField(upload_to='food_images/', verbose_name="食品图片")

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'foods'
        verbose_name = "食品"
        verbose_name_plural = verbose_name


class Order(models.Model):
    total_price = models.TextField()
    phone = models.TextField()
    name = models.TextField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id}'
    class Meta:
        db_table = 'order'
        verbose_name = "订单"
        verbose_name_plural = verbose_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.name}'
    class Meta:
        db_table = 'orderitem'
        verbose_name = "订单条目"
        verbose_name_plural = verbose_name

class RepairOrder(models.Model):
    name = models.CharField(max_length=100, verbose_name="姓名")
    phone_number = models.CharField(max_length=11, verbose_name="电话号码")
    address = models.TextField(verbose_name="地址")
    description_audio =  models.FileField(upload_to='descriptions/')

    def __str__(self):
        return f"{self.name} - {self.address}"

    class Meta:
        db_table = 'repairorder'
        verbose_name = "维修订单"
        verbose_name_plural = verbose_name

class Medication(models.Model):
    username = models.TextField(verbose_name="被提醒用户名")
    name = models.CharField(max_length=100, verbose_name="药品名称")
    reminder_time = models.TextField(verbose_name="提醒时间")
    image = models.ImageField(upload_to='medications/', blank=True, null=True, verbose_name="药品图片")
    audio = models.FileField(upload_to='audios/')
    def __str__(self):
        return f"{self.name} at {self.reminder_time.strftime('%H:%M')}"

    class Meta:
        db_table = 'medication'
        verbose_name = "用药提醒"
        verbose_name_plural = verbose_name
