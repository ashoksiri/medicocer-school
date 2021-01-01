from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render

from accounts.forms import LoginForm, UserForm, TeacherForm, StudentForm, BookForm
from accounts.models import User, Book

from django.shortcuts import redirect

import logging

log = logging.getLogger(__name__)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('school:login')
    # return render(request,'school/dashboard.html')
    if request.user.is_principal:
        return redirect('school:teachers')
    elif request.user.is_teacher:
        return redirect('school:students')
    else:
        return redirect('school:books')


def logout_user(request):
    logout(request)
    return redirect('school:login')


def login_user(request):
    form = LoginForm(request.POST or None)

    context = {
        'form': form
    }

    if request.user.is_authenticated:
        return redirect('school:index')

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('school:dashboard')
                # return render(request, 'school/dashboard.html',{'albums':albums})
            else:
                context.update({'error_message': 'Your account has been disabled'})
                return render(request, 'school/login.html', context)
        else:
            context.update({'error_message': 'Invalid username or Password.'})
            return render(request, 'school/login.html', context)

    return render(request, 'school/login.html', context)


def register(request):
    form = UserForm(request.POST or None)

    context = {
        "form": form,
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # user_data = {'username': username, 'email': email, 'password': password}
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('school:dashboard')
        except Exception as e:
            log.error(e.args)
            # context.update({'error_message':'user already exists ...'})
            return render(request, 'school/register.html', context)

    return render(request, 'school/register.html', context)


@login_required
def profile(request):
    return render(request, 'school/profile.html')


def get_teachers_with_students(loginuser):
    users = User.objects.filter(is_teacher=True, created_by=loginuser)
    teachers = []
    for user in users:
        teacher = model_to_dict(user)
        students = [model_to_dict(student)
                    for student in User.objects.filter(is_student=True, created_by=user)]
        teacher['students'] = students
        teachers.append(teacher)
    return teachers


def get_students_with_books(loginuser):
    if loginuser.is_principal:
        users = User.objects.filter(is_student=True,
                                    created_by__in=User.objects.filter(is_teacher=True, created_by=loginuser))
    else:
        users = User.objects.filter(is_student=True, created_by=loginuser)
    students = []
    for user in users:
        student = model_to_dict(user)
        books = [model_to_dict(student)
                    for student in Book.objects.filter(user=user)]
        student['books'] = books
        students.append(student)
    return students


@login_required
def teachers(request):
    form = TeacherForm(request.POST or None)

    context = {
        "form": form,
        'teachers': get_teachers_with_students(request.user)
    }

    if request.method == 'POST':
        password = request.POST.get('password')
        if form.is_valid():
            print(form.cleaned_data)
            teacher = form.save(commit=False)
            teacher.set_password(password)
            teacher.is_principal = False
            teacher.profile_picture = request.FILES['profile_picture']
            teacher.created_by = request.user
            teacher.save()
            context.update({'teachers': get_teachers_with_students(request.user)})
        else:
            context.update({'errors': form.errors})
            return render(request, 'school/add_teacher.html', context)

    return render(request, 'school/add_teacher.html', context)


@login_required
def students(request):
    form = StudentForm(request.POST or None)

    context = {
        "form": form,
        'students': get_students_with_books(request.user)
    }

    if request.method == 'POST':
        password = request.POST.get('password')
        if form.is_valid():
            print("add", form.cleaned_data)
            student = form.save(commit=False)
            student.set_password(password)
            student.profile_picture = request.FILES['profile_picture']
            student.is_principal = False
            student.created_by = request.user
            student.save()
            context.update({'students': get_students_with_books(request.user)})
        else:
            print(form.errors)
            context.update({'errors': form.errors})

    return render(request, 'school/add_students.html', context)


@login_required
def books(request):
    form = BookForm(request.POST or None)

    context = {
        "form": form,
        'books': Book.objects.filter(user=request.user)
    }

    if request.method == 'POST':

        if form.is_valid():
            print("add", form.cleaned_data)
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            context.update({'books': Book.objects.filter(user=request.user)})
        else:
            print(form.errors)
            context.update({'errors': form.errors})

    return render(request, 'school/add_books.html', context)
