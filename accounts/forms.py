

import unicodedata
from django import forms
from django.contrib.auth import authenticate
from django.forms import Widget, TextInput
from .models import User, Book


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))

class MyText(Widget):
    input_type = 'text'
    template_name = 'school/username.html'

class UserForm(forms.ModelForm):

    username = UsernameField(
        max_length=254,
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeHolder': 'Username',
                'autofocus': True}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeHolder': 'Password'}))

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeHolder': 'Retype Password'}))

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeHolder': 'Your Email'}))


    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class TeacherForm(UserForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'tclass', 'is_teacher', 'profile_picture']

class StudentForm(UserForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'tclass', 'is_student', 'profile_picture']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name','tclass', 'subject']

class LoginForm(forms.Form):

    username = UsernameField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeHolder': 'Username',
                'autofocus': True}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeHolder': 'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user