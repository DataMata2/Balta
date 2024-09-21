from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Shoe
from .forms import ShoeForm


def binarySearch(target_name):
    shoes = Shoe.objects.order_by('name')  # Retrieve all shoes from the table sorted by name
    low = 0
    high = len(shoes) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_name = shoes[mid].name

        if mid_name == target_name:
            return shoes[mid]  # Found a match
        elif mid_name < target_name:
            low = mid + 1
        else:
            high = mid - 1

    return None  # Name not found

def sortByName(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x.name < pivot.name]
    middle = [x for x in arr if x.name == pivot.name]
    right = [x for x in arr if x.name > pivot.name]

    return sortByName(left) + middle + sortByName(right)

def sortById(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x.id < pivot.id]
    middle = [x for x in arr if x.id == pivot.id]
    right = [x for x in arr if x.id > pivot.id]

    return sortById(left) + middle + sortById(right)

def home(request):
    context ={}
    return render(request, 'base/home.html', context)

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        context = {}
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password Are Not Correct')
    context = {}
    return render(request, 'base/login.html', context)

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    context = {'form': form}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'An error occured during registration')
            return redirect('register')
    return render(request, 'base/register.html', context)

@login_required(login_url = 'login')
def admin(request, q = ''):
    context = {}
    shoes = Shoe.objects.all()
    if request.GET.get('q'):
        q = request.GET.get('q')
        shoes = []
        shoes.append(binarySearch(q))
    elif(request.method == "POST" and 'sortById' in request.POST):
        shoes = sortById(shoes)
    elif(request.method == "POST" and 'sortByName' in request.POST):
        shoes = sortByName(shoes)
    context['shoes'] = shoes
    
    return render(request, 'base/a-side.html', context)

@login_required(login_url = 'login')
def create(request):
    form = ShoeForm()
    context = {'form' : form}
    if request.method == "POST":
        form = ShoeForm(request.POST)
        if form.is_valid():
            shoe = form.save(commit=False)
            shoe.name = shoe.name.lower()
            shoe.save()
            return redirect('a-side')
        else:
            messages.error(request, 'An error occured during adding shoe to a database')
            return redirect('create')
    return render(request, 'base/create.html', context)

@login_required(login_url = 'login')
def update(request, pk):
    shoe = get_object_or_404(Shoe, pk=pk) 
    if request.method == 'POST':
        form = ShoeForm(request.POST, instance=shoe)  # Bind the form data to the shoe object

        if form.is_valid():
            form.save()  # Save the updated shoe object
            return redirect('a-side')  # Redirect to the shoe's detail page
    else:
        form = ShoeForm(instance=shoe)  # Create a form instance with the shoe object
    context = {'form' : form, 'shoe' : shoe}
    return render(request, 'base/update.html', context)

def delete(request, pk):
    shoe = get_object_or_404(Shoe, pk=pk)  # Retrieve the shoe object
    shoe.delete()
    return redirect('a-side')
