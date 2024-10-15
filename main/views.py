from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdvertisementRequestForm
from .models import AdvertisementRequest, User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.functional import SimpleLazyObject

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
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']

        # Проверка на совпадение паролей
        if password != password_repeat:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'register.html')

        # Проверка, существует ли пользователь с таким логином
        if User.objects.filter(login=user_login).exists():
            messages.error(request, 'Пользователь с таким логином уже существует')
            return render(request, 'register.html')

        # Проверка, существует ли пользователь с таким email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'register.html')

        # Создание пользователя
        user = User.objects.create_user(login=user_login, email=email, password=password)
        user.save()

        # Вход пользователя после регистрации
        user = authenticate(request, login=user_login, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправляем на домашнюю страницу после успешной регистрации
        else:
            messages.error(request, 'Не удалось зайти в аккаунт')
            return redirect('login')
    return render(request, 'register.html')


def loginer(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        user_login = request.POST['login']
        password = request.POST['password']
        
        user = authenticate(request, login=user_login, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')  # Добавляем сообщение
            return redirect('home')  # Перенаправляем на домашнюю страницу
        else:
            messages.error(request, 'Неверные логин или пароль')
            return redirect('login')
    return render(request, 'login.html')

def success_page(request):
    return render(request, 'success_page.html')

@login_required
def advertisement_request_view(request):
    if request.method == 'POST':
        form = AdvertisementRequestForm(request.POST)
        if form.is_valid():
            user = request.user  # Получаем текущего пользователя
            if isinstance(user, SimpleLazyObject):
                user = user._wrapped  # Если пользователь ленивый объект, извлекаем реального пользователя

            ad_request = AdvertisementRequest(
                user=user,  # Передаем корректного пользователя
                ad_content=form.cleaned_data['ad_content']
            )
            ad_request.save()
            return redirect('success_page')  # Редирект на страницу успеха
    else:
        form = AdvertisementRequestForm()

    return render(request, 'advertisement_request.html', {'form': form})

def profile_view(request):
    # Получаем все заявки пользователя
    ad_requests = AdvertisementRequest.objects.filter(user=request.user)
    
    # Сообщение об успешном входе
    messages.success(request, f'Добро пожаловать, {request.user.login}!')

    return render(request, 'profile.html', {'ad_requests': ad_requests})

def logout_view(request):
    logout(request)
    messages.info(request, f'Вы вышли из аккаунта.') 
    return redirect('home')