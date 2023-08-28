from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        u_name = request.POST['username']
        f_name = request.POST['fname']
        l_name = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']

        if User.objects.filter(username=u_name):
            messages.error(request, 'User name taken, try another!!')
        elif User.objects.filter(email=email):
            messages.error(request, 'Email already registered!. Try another!.')
        elif password2 != password1:
            messages.error(request, 'Passwords do not match!')
        else:
            app_user = User.objects.create_user(u_name, email, password1)
            app_user.first_name = f_name
            app_user.last_name = l_name
            app_user.is_Active = True
            app_user.save()

            messages.success(request, 'Account created successfully!!')

            return redirect('signin')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        u_name = request.POST['username']
        password1 = request.POST['pass1']

        user = authenticate(username=u_name, password=password1)

        if user is not None:
            login(request, user)
            u_name = user.username
            f_name = user.first_name
            l_name = user.last_name

            return render(request, 'index.html', {'u_name': u_name, 'f_name': f_name, 'l_name': l_name})
        else:
            messages.error(request, 'Invalid credentials, please try again!!')

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'You have logged out successfully!!')
    return redirect('index')
    # return render(request, 'index.html')
