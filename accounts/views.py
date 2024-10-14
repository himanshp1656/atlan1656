# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home(request):


    
    return render(request, 'customer/home.html')
# Registration view
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User, Group
# Registration view
def register(request):
    if request.method == 'POST':
        print('Form submitted.')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(username, email, password1, password2)

        # Validate passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'accounts/register.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'accounts/register.html')

        # Create a new user instance
        user = User(username=username, email=email)
        user.set_password(password1)  # Set hashed password
        user.save()  # Save the user to the database
        customer_group, created = Group.objects.get_or_create(name='customer')
        user.groups.add(customer_group)
        # Authenticate and log in the user
        user = authenticate(username=username, password=password1)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('/customer/book/')
        else:
            messages.error(request, "Authentication failed. Please try again.")

    return render(request, 'accounts/register.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            # Check if the user belongs to the "customer" group
            if user.groups.filter(name='customer').exists():
                return redirect('customer_home')  # Redirect to customer home page

            # Check if the user belongs to the "driver" group
            elif user.groups.filter(name='driver').exists():
                return redirect('driver_home')  # Redirect to driver home page
            
            else:
                messages.error(request, 'User does not belong to any valid group.')
                return redirect('login')

        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
