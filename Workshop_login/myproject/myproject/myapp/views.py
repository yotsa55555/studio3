from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, RecordForm
from .models import Record

def home(request):
    return render(request, 'myapp/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('records')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid credentials')
    form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

@login_required
def records(request):
    user_records = Record.objects.filter(user=request.user)
    all_records = Record.objects.all()
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('records')
    else:
        form = RecordForm()
    return render(request, 'myapp/records.html', {'user_records': user_records, 'all_records': all_records, 'form': form})

@login_required
def edit_record(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if record.user != request.user:
        return redirect('records')
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('records')
    else:
        form = RecordForm(instance=record)
    return render(request, 'myapp/edit_record.html', {'form': form})

