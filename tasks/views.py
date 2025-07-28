from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import TaskForm 
from .models import Task

# Create your views here.
# --- HOME

def Home(request):
    return render(request, 'home.html')

# --- LOGIN

def Signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm,'error': 'User already exist'})

        return render(request, 'signup.html', {'form': UserCreationForm,'error': 'password do not match'})

def Signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm,'error': 'User or password are incorrect'})
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def Signout(request):
    logout(request)
    return redirect('home')

# --- TASKS

@login_required
def Tasks(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'tasks.html',{'tasks': task})

@login_required
def TasksCompleted(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'task-completed.html',{'tasks': task})

@login_required
def CreateTask(request):

    if request.method == "GET":
        return render(request, 'create-task.html', {'form': TaskForm })
    else:
        form = TaskForm(request.POST)
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect('tasks')       

@login_required
def TaskDetail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task,pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task-detail.html', {'task': task,'form': form})
    else:
        try:
            task = get_object_or_404(Task,pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task-detail.html', {'task': task,'form': form,'error': "Error updating task"})

@login_required
def TaskComplete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def TaskDelete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')

