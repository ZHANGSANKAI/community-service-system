#@Time:  10:14
#@Author: 左 恒
#@File:form.py
#@software: PyCharm

# forms.py

from django import forms
from .models import Food, Medication
from .models import RepairOrder
import re

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'category', 'price', 'sels', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'sels': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }



class RepairOrderForm(forms.ModelForm):
    class Meta:
        model = RepairOrder
        fields = ['name', 'phone_number', 'address', 'description_audio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'description_audio': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # 验证电话格式为11位数字
        if not re.match(r'^\d{11}$', phone_number):
            raise forms.ValidationError("电话号码必须为11位数字。")
        return phone_number



class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'reminder_time', 'image', 'username']
