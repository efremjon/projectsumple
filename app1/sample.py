from unicodedata import name
from django.shortcuts import redirect, render
from .models import *
from .form import OrderForm,CreateUser,CustomerForm
from django.forms import inlineformset_factory 
from .filetr import Oredefilters
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group 

# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user,)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'account/reg.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        cheekuser=authenticate(request, username=username,password=password)
        if cheekuser is not None:
            login(request,cheekuser)
            return redirect('/')
        else:
            messages.success(request, 'Username or password is incorrect')
    return render(request,'account/login.html')

def logoutUser(request):
    logout(request)
    return redirect ('login')
    
@login_required(login_url='login')
@admin_only
def home(request):
    customers=Customer.objects.all()
    Orders=Order.objects.all()
    total_customer=customers.count()
    total_order=Orders.count()
    Deliverd=Orders.filter(status='Delivered').count()
    pending=Orders.filter(status='Pending').count()
    context={
        'customers':customers,
        'Orders':Orders,
        'total_order':total_order,
        'total_customer':total_customer,
        'Deliverd':Deliverd,
        'pending':pending,
    }
   
    return render(request,'account/dashbord.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    Orders=request.user.customer.order_set.all()
    total_order=Orders.count()
    Deliverd=Orders.filter(status='Delivered').count()
    pending=Orders.filter(status='Pending').count()
    context = {
               'Orders':Orders,
               'total_order':total_order,
               'Deliverd':Deliverd,
               'pending':pending,
    }
    return render(request, 'account/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()
	context = {'form':form}
	return render(request, 'account/account_setting.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products= Product.objects.all()
    return render(request,'account/product.html',{'products':products})

@login_required(login_url='login')
def customer(request,pk_cust):
    customer=Customer.objects.get(pk=pk_cust)
    Cust_Order=customer.order_set.all()
    total_order=Cust_Order.count()
    MyFileter=Oredefilters(request.GET,queryset=Cust_Order)
    Cust_Order=MyFileter.qs
    context={
        'customer':customer,
        'Cust_Order':Cust_Order,
        'total_order':total_order,
        'MyFileter':MyFileter,
    }
    return render(request,'account/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Customer_Order(request, pk):
    OrdeFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=1)
    customersel=Customer.objects.get(pk=pk)
    formset=OrdeFormSet(queryset=Order.objects.none(), instance=customersel)
    
    if request.method == 'POST':
       
        formset=OrdeFormSet(request.POST,instance=customersel)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={
        'formset':formset
    }
    return render(request,'account/customer_order.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def Update_Order(request, pk):

    order=Order.objects.get(pk=pk)

    if request.method == 'POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=OrderForm(instance=order)
    context={
        'form':form
    }
    return render(request,'account/customer_order.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def Delete_Order(request, pk):

    item=Order.objects.get(pk=pk)

    if request.method == 'POST':

        item.delete()
        return redirect('/')
    else:
        pass
    
    return render(request,'account/delete.html',{'item':item})