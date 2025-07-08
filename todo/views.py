from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import RegisterForm, TaskForm
from .models import Task
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        users = User.objects.all()
        tasks = Task.objects.all()
        return render(request, 'admin_dashboard.html', {'users': users, 'tasks': tasks})
    else:
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'home.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

@login_required
def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_complete = not task.is_complete
    task.save()
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')
