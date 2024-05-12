"""my01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    #请求路径和视图函数之间的映射关系,一旦请求
    path('admin/', admin.site.urls),
    path("register/",views.get_register),
    path("",views.get_login,name='success_page'),
    path("serverpage/",views.get_serverpage,name='success_page2'),
    path("customerpage/",views.get_customerpage,name='success_page1'),
    path('customerpage/personal.html', views.personal_view, name='personal_page'),
    path('serverpage/personal.html', views.personal_view, name='personal_page1'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('serverpage/dinnerup.html', views.dinnerup, name='dinnerup'),
    path('customerpage/dinnerpage',views.dinnerpage,name='dinnerpage'),
    path('customerpage/order.html',views.order,name='order'),
    path('serverpage/dinnermanage.html',views.dinnermanage,name='dinnermanage'),
    path('serverpage/foodmanage.html', views.foodmanage, name='foodmanage'),
    path('serverpage/foodmanage/deleteconfirm/<int:id>/', views.deleteconfirm, name='deleteconfirm'),
    path('serverpage/foodmanage/foodedit/<int:id>/', views.foodedit, name='foodedit'),
    path('customerpage/homeprotect', views.homeprotect, name='homeprotect'),
    path('serverpage/protectmanage.html', views.protectmanage, name='protectmanage'),
    path('serverpage/protectmanage/<int:order_id>/', views.delete_protect, name='delete_protect'),
    path('customerpage/mreminder', views.mreminder, name='mreminder'),
    path('serverpage/medicationup.html', views.medicationup, name='medicationup'),
    path('serverpage/medicationmanage.html',views.medicationmanage,name='medicationmanage'),
    path('logout', views.logout_view, name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
