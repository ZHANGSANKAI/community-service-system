import io
import json
import os
from decimal import Decimal, InvalidOperation

import pyttsx3
import requests
from bs4 import BeautifulSoup
from django.core import serializers
from django.core.files.base import ContentFile, File
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_POST
from pydub import AudioSegment

from .form import FoodForm, RepairOrderForm, MedicationForm
from .models import User, Food, Order, OrderItem, RepairOrder, Medication
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
import logging
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.contrib import messages
from gtts import gTTS

# Create your views here.
@login_required
def get_serverpage(request):
    if not request.user.is_authenticated:

        return redirect('success_page')
    return render(request, 'admin/serverpage.html')

@login_required
def get_customerpage(request):
    if not request.user.is_authenticated:
        # 如果用户未登录，可以重定向到登录页面或者显示错误消息
        return redirect('success_page')  # 'login_url'是登录页面的url名称，需要根据你的实际情况进行修改

    username = request.user.username
    return render(request, 'users/customerpage.html', {"username": username})



# 设置日志
logger = logging.getLogger(__name__)

def get_login(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usertype = request.POST.get('usertype')
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                # 验证用户类型和 is_superuser 字段是否匹配
                if (user.is_superuser and usertype == 'service') or (not user.is_superuser and usertype == 'user'):
                    login(request, user)
                    logger.info(f"Logged in user type for {username}: {usertype}")
                    if user.is_superuser:
                        return redirect('success_page2')  # 重定向到管理员页面
                    else:
                        return redirect('success_page1')  # 重定向到普通用户页面
                else:
                    error_message = "登录失败，用户类型不匹配。"
                    logger.error(error_message)
                    return render(request, 'users/login.html', {'error_message': error_message})
            else:
                error_message = "登录失败，请检查密码。"
                logger.error(error_message)
                return render(request, 'users/login.html', {'error_message': error_message})
        except User.DoesNotExist:
            error_message = "用户不存在，请检查用户名。"
            logger.error(error_message)
            return render(request, 'users/login.html', {'error_message': error_message})
    else:
        # 对于非POST请求，如GET请求，返回登录页面
        return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
        # 用户退出后重定向到登录页面或主页
    return redirect('success_page1')

# 注册的视图函数
def get_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phonenumber = request.POST.get('phonenumber')
        password = request.POST.get('password')
        address = request.POST.get('address')

        # 使用 make_password 进行密码哈希
        hashed_password = make_password(password)

        try:
            # 创建并保存用户对象到数据库
            user = User(username=username, phonenumber=phonenumber, password=hashed_password, address=address)
            user.save()

            # 可以进行其他操作，例如登录用户等

            return redirect('success_page')  # 重定向到注册成功页面
        except Exception as e:
            # 处理保存失败的情况，可以记录日志或者向用户显示错误信息
            print(f"Error saving user: {e}")
            error_message = "注册失败，请重试或联系管理员。"
            return render(request, 'users/register.html', {'error_message': error_message})

    else:
        # 对于非POST请求，如GET请求，返回注册页面
        return render(request, 'users/register.html')


@login_required
def personal_view(request):
    user = request.user
    context = {'user': user}
    if request.method == 'POST':
        user.phonenumber = request.POST.get('phonenumber', user.phonenumber)  # 获取新号码或默认当前号码
        user.address = request.POST.get('address', user.address)  # 获取新地址或默认当前地址

        # 处理密码更改
        current_password = request.POST.get('current-password')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        if new_password and confirm_password and current_password:
            if new_password == confirm_password:
                if user.check_password(current_password):  # 验证当前密码是否正确
                    user.set_password(new_password)  # 更新密码
                    update_session_auth_hash(request, user)  # 重要：更新session以防止用户登出
                else:
                    messages.error(request, '当前密码不正确。')
                    return redirect('personal_page')  # 返回个人中心页面以重新输入
            else:
                messages.error(request, '新密码和确认密码不匹配。')
                return redirect('personal_page')  # 返回个人中心页面以重新输入

        user.save()  # 保存用户对象，更新数据库中的信息
        messages.success(request, '您的信息已更新。')
        return redirect('personal_page')  # 重定向到个人中心页面
    else:
        return render(request, 'users/personal.html', context)




# 添加购物车的视图函数

def dinnerup(request: HttpRequest):
    if request.method == 'POST':
        # 从POST数据中获取信息
        name = request.POST.get('foodname')
        price = request.POST.get('foodprice')
        category = request.POST.get('foodcategory')  # 假设表单中有一个分类输入
        image = request.FILES.get('foodpicture')  # 获取上传的图片
        sels = request.POST.get('fooddescribe')

        try:
            # 创建并保存食品对象到数据库
            food = Food(name=name, category=category, price=price, sels=sels, image=image)
            food.save()
            return redirect('dinnerup')  # 重定向到某个页面，确认 'dinnerup' 是正确的URL名称
        except Exception as e:
            print(f"Error saving food: {e}")
            error_message = "上传失败，请重试或联系管理员。"
            return render(request, 'admin/dinnerup.html', {'error_message': error_message})

    else:
        # 对于非POST请求，如GET请求，返回上传页面
        return render(request, 'admin/dinnerup.html')


def dinnerpage(request):
    if request.method == 'GET':
        items = {
            "肉品": [
                {"id": str(product.id), "name": product.name, "cls": product.category, "price": product.price, "sels": product.sels, "imageUrl": product.image.url}
                for product in Food.objects.filter(category="肉类")
            ],
            "水产": [
                {"id": str(product.id), "name": product.name, "cls": product.category, "price": product.price, "sels": product.sels, "imageUrl": product.image.url}
                for product in Food.objects.filter(category="水产")
            ],
            "蔬菜": [
                {"id": str(product.id), "name": product.name, "cls": product.category, "price": product.price,
                 "sels": product.sels, "imageUrl": product.image.url}
                for product in Food.objects.filter(category="蔬菜")
            ],
            "主食": [
                {"id": str(product.id), "name": product.name, "cls": product.category, "price": product.price,
                 "sels": product.sels, "imageUrl": product.image.url}
                for product in Food.objects.filter(category="主食")
            ],
            "其它": [
                {"id": str(product.id), "name": product.name, "cls": product.category, "price": product.price,
                 "sels": product.sels, "imageUrl": product.image.url}
                for product in Food.objects.filter(category="其它")
            ],
        }
        print(items)
        return render(request, 'users/dinnerpage.html', {'items': items})
    if request.method == 'POST':
        # 获取POST请求中的数据
        print(request.POST)
        item1 = request.POST.getlist('item')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        address = request.POST.get('address')

        parts = item1[0].split(',')
        total_price = parts[-1]
        parts.pop()
        half_length = len(parts) // 2
        first_half = parts[:half_length]
        second_half = parts[half_length:]
        items = [first_half, second_half]

        print(items)

        if not (total_price and phone and name and address):
            return JsonResponse({'error': '订单信息不完整'}, status=400)

        order = Order( total_price=total_price,phone=phone,name=name,address=address)
        order.save()

        # 将商品信息存储到关联的订单详情表中
        count=0
        while count<(len(items[0])):
            item_name = items[0][count]
            item_quantity = int(items[1][count])
            orderitem = OrderItem(order=order,name=item_name,quantity=item_quantity)
            orderitem.save()
            count = count + 1

        # 返回JSON响应表示订单已成功提交
        return redirect('order')
    else:
        return JsonResponse({'error': '只接受POST请求'}, status=400)



def order(request):
    if request.user.is_authenticated:
        user_name = request.user.username  # 获取用户名

    # 获取所有该用户名下的订单
    orders = Order.objects.filter(name=user_name)

    # 准备数据字典
    data = []

    # 遍历每个订单
    for order in orders:
        order_data = {
            'order_id': order.id,
            'total_price': order.total_price,
            'items': []
        }

        # 获取每个订单的所有订单项
        order_items = order.items.all()

        # 遍历订单项
        for item in order_items:
            # 通过订单项名称找到对应的食品
            try:
                food = Food.objects.get(name=item.name)
                food_price = food.price
            except Food.DoesNotExist:
                food_price = "Unavailable"

            # 添加订单项信息到列表
            order_data['items'].append({
                'name': item.name,
                'quantity': item.quantity,
                'food_price': food_price
            })

        # 添加当前订单数据到总数据列表
        data.append(order_data)

    # 渲染模板或返回JSON数据
    return render(request, 'users/order.html', {'orders_data': data})


def dinnermanage(request):
    if request.method == 'GET':
        # 准备数据字典
        data = []

        orders = Order.objects.all()

        # 遍历每个订单
        for order in orders:
            order_data = {
                'username' : order.name,
                'address' : order.address,
                'phonenumber' : order.phone,
                'order_id': order.id,
                'total_price': order.total_price,
                'items': []
            }

            # 获取每个订单的所有订单项
            order_items = order.items.all()

            # 遍历订单项
            for item in order_items:
                # 通过订单项名称找到对应的食品
                try:
                    food = Food.objects.get(name=item.name)
                    food_price = food.price
                except Food.DoesNotExist:
                    food_price = "Unavailable"

                # 添加订单项信息到列表
                order_data['items'].append({
                    'name': item.name,
                    'quantity': item.quantity,
                    'food_price': food_price
                })

            # 添加当前订单数据到总数据列表
            data.append(order_data)

        # 渲染模板或返回JSON数据
        return render(request, 'admin/dinnermanage.html', {'orders_data': data})
    else:
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return redirect('dinnermanage')  # 重定向到订单列表页
        except Order.DoesNotExist:
            return HttpResponse('Order not found', status=404)


def foodmanage(request):
    foods = Food.objects.all()
    return render(request, 'admin/foodmanage.html', {'foods': foods})

def deleteconfirm(request, id):
    food = get_object_or_404(Food, pk=id)
    if request.method == 'POST':
        food.delete()
        return redirect('foodmanage')
    else:
        return render(request, 'admin/deleteconfirm.html', {'food': food})

def foodedit(request, id):
    food = get_object_or_404(Food, id=id)
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            return redirect('foodmanage')
    else:
        form = FoodForm(instance=food)
    return render(request, 'admin/foodedit.html', {'form': form, 'food': food})


def homeprotect(request):
    if request.method == 'POST':
        form = RepairOrderForm(request.POST, request.FILES)
        if form.is_valid():
            # 保存表单数据到数据库
            form.save()
            return redirect('homeprotect')  # 重定向到成功页面
        else:
            return HttpResponse("Invalid data", status=400)
    else:
        form = RepairOrderForm()
    return render(request, 'users/homeprotect.html', {'form': form})


def protectmanage(request):
    """ 显示所有订单 """
    orders = RepairOrder.objects.all()
    return render(request, 'admin\protectmanage.html', {'orders': orders})

@require_POST
def delete_protect(request, order_id):
    """ 删除指定的订单 """
    order = RepairOrder.objects.get(id=order_id)
    order.delete()
    return redirect('protectmanage')


def mreminder(request):
    medications = Medication.objects.filter(username=request.user.username)

    return render(request, 'users/mreminder.html', {'medications': medications})


def medicationup(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST, request.FILES)
        if form.is_valid():
            medication = form.save(commit=False)

            # 初始化语音引擎
            engine = pyttsx3.init()
            text = f"{medication.name}, 提醒时间 {medication.reminder_time}"

            # 生成临时音频文件
            audio_filename = 'temp.wav'
            engine.save_to_file(text, audio_filename)
            engine.runAndWait()  # 确保音频生成完成

            # 保存音频文件到指定的上传路径
            with open(audio_filename, 'rb') as wav_file:
                medication.audio.save(f"{medication.name}.wav", File(wav_file), save=False)

            # 删除临时文件
            os.remove(audio_filename)

            # 保存表单数据到数据库
            medication.save()

            return redirect('medicationup')  # 或其他适合的重定向
    else:
        form = MedicationForm()

    return render(request, 'admin/medicationup.html', {'form': form})


# def medicationmanage(request):
#     return render(request, 'admin/medicationmanage.html')

def medicationmanage(request):
    if request.method == 'POST':
        # 处理删除操作
        medication_id = request.POST.get('medication_id')
        if medication_id:
            medication = get_object_or_404(Medication, id=medication_id)
            medication.delete()
            return redirect('medicationmanage')  # 删除后重定向到列表页面

    # GET 请求处理: 显示用药提醒列表
    medications = Medication.objects.all()
    return render(request, 'admin/medicationmanage.html', {'medications': medications})