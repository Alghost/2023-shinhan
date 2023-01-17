from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def signin(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        User.objects.create_user(
            request.POST.get('user_id'),
            request.POST.get('email'),
            request.POST.get('password')
        )
        return redirect('/member/login/')

    return render(request, 'register.html')