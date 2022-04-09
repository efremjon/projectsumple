from multiprocessing import context
from urllib import request
from django.shortcuts import redirect, render
from .form import CreateUser
from django.contrib import messages
from django.contrib.auth.models import User ,Group,auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from Agent.views import Agent_page

def home(request):

    return render(request,'home.html',{})

#this is registration and login 
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        user_name=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'username taken')
                return render(request,'reg.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email taken ')
                return render(request,'reg.html')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,email=email,password=password1)
                user.save()
                group = Group.objects.get(name='Customer')
                user.groups.add(group)
                messages.info(request, 'Sucssesfull Create User')
                return redirect ('login')
        else:
            print('user is not crated')
            return render(request,'reg.html')
    else:
        # raise ValidationError("User Already Exist")
        messages.info(request, 'password not match') 
        return render(request,'reg.html')

@unauthenticated_user
def login_view(request):
    
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username,password=password)
        a=user.groups.all()[0].name
        if a == 'Admin':
            login(request,user)
            return redirect('admin-dashbord',)
        elif a == 'Agent':
            login(request,user)
            return redirect('agent-dashbord')
        elif a == 'Customer':
            login(request,user)
            return redirect('customer_page')

    return render(request,'login.html')
def logout_view(request):
    logout(request)
    return redirect('/')

##user-page 
@login_required
def Customer_page(request):
    groups=Group.objects.all()
    egroup = request.user.groups.all()
    return render(request, 'customer-dashbord.html',{})

# @login_required
# def Agent_page(request):
#     return render(request, 'agent_dashbord.html',{})
# ## end user page

@login_required
def Admin_page(request):
    return render(request,'admin-dashbord.html',{})

