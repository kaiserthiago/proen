from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from login.forms import RegistroForm


def register(request):
    if request.method == 'POST':
        user_form = RegistroForm(request.POST)

        if user_form.is_valid():
            User.objects.create_user(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'],
                email=user_form.cleaned_data['email'],
                first_name=user_form.cleaned_data['first_name'],
                # last_name=user_form.cleaned_data['last_name'],
                is_active=True,
            )

            return redirect('home')

    user_form = RegistroForm()

    context = {
        'user_form': user_form,
    }
    return render(request, 'registration/templates/login/login.html', context)


def user_login(request):
    if request.user.is_anonymous and request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.POST['next']:
                return redirect(request.POST['next'])
            else:
                return redirect('home')
        else:
            messages.error(request, 'Usuário e/ou senha inválidos')
            return redirect('login')
    else:
        return render(request, 'login/login.html', {})


def user_logout(request):
    logout(request)
    return redirect('home')