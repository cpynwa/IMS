from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


# Create your views here.

# IMS 로그인 시스템
def WMS_signup(request):
    if request.method == "POST":
        if request.POST["password"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password"])
            auth.login(request, user)
            return redirect('/IMS/login')
        return render(request, 'account/signup.html')
    return render(request, 'account/signup.html')

def WMS_login(request):
    if request.session.session_key:
        return redirect('/IMS/main')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/IMS/main')
            else:
                return render(request, 'account/login.html', {'error': 'username or password in incorrect'})
        else:
            return render(request, 'account/login.html')


def WMS_logout(request):
    auth.logout(request)
    return redirect('/IMS/login')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/IMS/login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {'form': form})
