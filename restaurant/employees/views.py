from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import EmployeeInfoForm, UpdateEmployeeForm, NewEmployeeForm, ChangePasswordForm

# Create your views here.
@login_required(login_url='employees:login')
def update_profile(request):
    if request.method == 'POST':
        form = UpdateEmployeeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('employees:profile')
    else:
        form = UpdateEmployeeForm(instance=request.user)

@login_required(login_url='employees:login')
def update_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('employees:profile')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'employees/update_password.html', {'form': form})

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = NewEmployeeForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('home')
    else:
        form = NewEmployeeForm()
    return render(request, 'employees/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'employees/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("employees:login")
    return render(request, 'employees/logout.html')

@login_required(login_url='employees:login')
def profile_view(request):
    if request.method == 'POST':
        form = EmployeeInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('employees:profile')
    else:
        form = EmployeeInfoForm(instance=request.user)
    return render(request, 'employees/profile.html', {'form': form})