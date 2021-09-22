from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.decorators import login_required,user_passes_test
from . import forms
import random
from django.db.models import Q
from django.apps import apps
import accounts
# Create your views here.
# fetch all pomps
def pomplist(request):
    key=''
    if accounts.views.is_customer(request.user):
        key='2'
    else:
        key='1'
    ps=models.pomps.objects.all().order_by('brand')
    args={'pomps':ps,'key':key}
    return render(request,'pomp/pomplist.html',args)
#fetch a pomp's details
def pompdetail(request,slugg):
    key=''
    if accounts.views.is_customer(request.user):
        key='2'
    else:
        key='1'
    p=models.pomps.objects.get(slug=slugg)
    args={'pomp':p,'key':key}
    return render(request,'pomp/pompdetail.html',args)

#create a new pomp
@login_required(login_url="/accounts/customerlogin")
def create_pomp(request):
    if request.POST:
        form=forms.CreatePomp(request.POST,request.FILES)
        if form.is_valid:
            instance=form.save(commit=False)
            instance.slug=create_slug()
            instance.author=request.user
            instance.save()
            return redirect('pompsale:listp')
    else:
        form=forms.CreatePomp()
    return render(request,'pomp/createPomp.html',{'form':form})

def create_slug():
    s=''
    n1=random.randint(63,97)
    s+=chr(n1)
    n2=random.randint(63,97)
    s+=chr(n2)
    n3=random.randint(63,97)
    s+=chr(n3)
    n4=random.randint(63,97)
    s+=chr(n4)
    n4=random.randint(63,97)
    s+=chr(n4)
    return s
#search a product in ppomp model in every page
def search_view(request):
    query=request.GET['query']
    prodeucts=models.pomps.objects.all().filter(Q(brand__icontains=query)|Q(modelnum__icontains=query)|Q(madein__icontains=query))
    key=''
    if accounts.views.is_customer(request.user):
        key='2'
    else:
        key='1'
    args={'pomps':prodeucts,'key':key}
    return render(request,'pomp/pomplist.html',args)
#register an order by Customer
@login_required(login_url='accounts/customerlogin')
# @user_passes_test('/accounts/afterlogin_view')
def order_register(request,idkey):
    neworder=models.order.objects.create()
    neworder.customer=apps.get_model('accounts','Customer').objects.get(user=request.user)
    neworder.product=models.pomps.objects.get(id=idkey)
    q=int(request.GET['qty'])
    neworder.quantity=q
    p=int(neworder.product.price)
    tp=q * p
    neworder.totalprice= tp
    neworder.save()
    return ordered_product(request)

@login_required(login_url='accounts/customerlogin')
def ordered_product(request):
    orders=models.order.objects.all().filter(customer_id=apps.get_model('accounts','Customer').objects.get(user=request.user))
    ordered_products=[]
    for order in orders:
        ordered_product=models.pomps.objects.all().filter(id=order.product_id)
        ordered_products.append(ordered_product)
    return render(request,'pomp/orderedproduct.html',{'data':zip(orders,ordered_products)})

#delete orderedproduct by customer
@login_required(login_url='accounts/customerlogin')
def delete_ordered_product(request,pk):
    order=models.order.objects.get(id=pk)
    order.delete()
    return redirect('pompsale:orderedproducts')
#show all product
@login_required(login_url='accounts/customerlogin')
def show_all_procuct(request):
    products=models.pomps.objects.all()
    return render(request,'pomp/allproduct.html',{'products':products})
#delete a product
@login_required(login_url='accounts/customerlogin')
def delete_product(request,pk):
    product=models.pomps.objects.get(id=pk)
    product.delete()
    return redirect('pompsale:showallproduct')
#show all orders
@login_required(login_url='accounts/customerlogin')
def all_ordered_product(request):
    orders=models.order.objects.all()
    # orders.group_by=['customer_id']
    ordered_products=[]
    customer_ordereds=[]
    for order in orders:
        ordered_product=models.pomps.objects.all().filter(id=order.product_id)
        ordered_products.append(ordered_product)
        customer_ordered=apps.get_model('accounts','Customer').objects.all().filter(id=order.customer_id)
        customer_ordereds.append(customer_ordered)

    return render(request,'pomp/allorderedproduct.html',{'data':zip(orders,customer_ordereds,ordered_products)})

#show all order for admin using customer id
@login_required(login_url='accounts/customerlogin')
def show_all_customer_ordered(request,ck):
    orders=models.order.objects.all().filter(customer_id=ck)
    ordered_products=[]
    for order in orders:
        ordered_product=models.pomps.objects.all().filter(id=order.product_id)
        ordered_products.append(ordered_product)
    return render(request,'pomp/customerordereds.html',{'data':zip(orders,ordered_products)})

#delete order bu admin
@login_required(login_url='accounts/customerlogin')
def delete_customer_ordered(request,pk):
    order=models.order.objects.get(id=pk)
    ck=order.customer_id
    order.delete()
    return redirect('pompsale:customerordereds',ck)
