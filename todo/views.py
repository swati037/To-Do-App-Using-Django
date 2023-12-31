from .forms import RegistrationForm
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import TodoTask

from django.contrib.auth import authenticate, login
from .forms import LoginForm

from django.shortcuts import render, redirect, get_object_or_404

from .forms import TodoTaskForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout



def landing(request):
    return render(request, 'landing.html')



import re  
def register_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        form = UserCreationForm(request.POST)

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'User already exists'})
        
        if password1 != password2:
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})

        if len(password1) < 8:
            return render(request, 'register.html   ', {'error_message': 'Password must be at least 8 characters long.'})

        if not re.search(r'\d', password1):
            return render(request, 'register.html', {'error_message': 'Password must contain at least one digit.'})

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            return render(request, 'register.html', {'error_message': 'Password must contain at least one special character.'})
  
        if form.is_valid():    
            user = form.save()
            login(request, user)
            
            return redirect('todo_list')
        else:
            return render(request, 'register.html', {'form': form})
        
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})




# def welcome_view(request, username):
#     return render(request, 'welcome.html', {'username': username})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if not User.objects.filter(username=username).exists():
                messages.error(request, 'User does not exist. Please register first.')
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('todo_list')
                else:
                    messages.error(request, 'Invalid password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



def todo_list(request):
    if request.user.is_authenticated:
        username = request.user.username
        tasks = TodoTask.objects.filter(user=request.user)
        return render(request, 'todo_list.html', {'tasks': tasks, 'username': username})
    else:
        return render(request, 'landing.html', {'error_message': 'Unauthorized user. Please register or log in.'})



def create_task(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TodoTaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user  
                task.save()
                return redirect('todo_list')
        else:
            form = TodoTaskForm()
    else:
        return render(request, 'landing.html', {'error_message': 'Unauthorized user. Please register or log in.'})
    
    return render(request, 'create_task.html', {'form': form})


def update_task(request, pk):
    task = get_object_or_404(TodoTask, pk=pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TodoTaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('todo_list')
        else:
            form = TodoTaskForm(instance=task)
    else:
        return render(request, 'landing.html', {'error_message': 'Unauthorized user. Please register or log in.'})
    
    return render(request, 'update_task.html', {'form': form, 'task': task})


def delete_task(request, pk):
    task = get_object_or_404(TodoTask, pk=pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            task.delete()
            return redirect('todo_list')
    else:
        return render(request, 'landing.html', {'error_message': 'Unauthorized user. Please register or log in.'})
    
    return render(request, 'delete_task.html', {'task': task})



def logout_view(request):
    logout(request)
    return redirect('landing')


