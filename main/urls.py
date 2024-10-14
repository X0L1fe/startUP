from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("about/", views.about, name='about'),
    path("register/", views.register, name='register'),
    path("login/", views.loginer, name='login'),
    path('success/', views.success_page, name='success'),
    path('advertisement-request/', views.advertisement_request_view, name='advertisement_request'),
    path('registering/', views.register_view, name='registering'),
    path('logining/', views.login_view, name='logining'),
]