from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdvertisementRequestForm
from .models import AdvertisementRequest
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def index(request):
    #return HttpResponse("Hello, world! This is my first Django application.")
    return render(request, 'index.html')

def about(request):
    #return HttpResponse("This is the about page.")
    return render(request, 'about.html')

def register(request):
    return render(request, 'register.html')

def register_view(request):
    if request.method == 'POST':
        user_login = request.POST['login']
    user_email = request.POST['email']
    password = request.POST['password']
    password_repeat = request.POST['password_repeat']

    if password != password_repeat:
        messages.error(request, 'Пароли не совпадают')
        return render(request, 'register.html')

    if User.objects.filter(username=user_login).exists():
        messages.error(request, 'Пользователь с таким логином уже существует')
        return render(request, 'register.html')

    if User.objects.filter(email=user_email).exists():
        messages.error(request, 'Пользователь с таким email уже существует')
        return render(request, 'register.html')

    user = User.objects.create_user(username=user_login, email=user_email, password=password)
    user.save()

    # Вход пользователя после регистрации
    user = authenticate(request, username=user_login, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')  # Перенаправляем на домашнюю страницу после успешной регистрации

    return render(request, 'register.html')

def loginer(request):
    return render(request, 'log.html')



def login_view(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']

        user = authenticate(request, username=login, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправляем на домашнюю страницу
        else:
            messages.error(request, 'Неверные логин или пароль')

    return render(request, 'login.html')

def success_page(request):
    return render(request, 'success_page.html')

@login_required
def advertisement_request_view(request):
    if request.method == 'POST':
        form = AdvertisementRequestForm(request.POST)
        if form.is_valid():
            ad_request = AdvertisementRequest(
                user=request.user,
                ad_content=form.cleaned_data['ad_content']
            )
            ad_request.save()
            return redirect('success_page')  # Редирект на страницу успеха
    else:
        form = AdvertisementRequestForm()

    return render(request, 'advertisement_request.html', {'form': form})