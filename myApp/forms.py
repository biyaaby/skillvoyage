from django import forms
from .models import *

class TeacherRequestForm(forms.ModelForm):
    class Meta:
        model = TeacherRequest
        fields = ['full_name', 'email', 'phone_number', 'qualification', 'experience_years', 'skills', 'resume']


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'short_description', 'description', 'price', 'sub_category', 'duration', 'learning_outcome', 'featured_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'instructor': forms.Select(attrs={'class': 'form-control'}),
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'learning_outcome': forms.Textarea(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-field'}),
        }


class CourseLessonForm(forms.ModelForm):
    class Meta:
        model = CourseLesson
        fields = ['title', 'description', 'resource']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'resource': forms.FileInput(attrs={'class': 'form-field'}),
        }


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'short_description', 'description', 'price', 'image', 'stock', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-field'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }