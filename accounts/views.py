
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout
from . import forms
from django.http import HttpResponseRedirect,HttpResponse
from . import models
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from django.apps import apps
# Create your views here.
def signup_user(request):
    if request.method == 'POST':
        form=forms.CreateUserForm(request.POST)

        if form.is_valid():
            try:
                user=form.save()
                login(request,user)
                return render(request,'accounts/successregister.html')
            except:
                pass

    else:
        form=forms.CreateUserForm()
    return render(request,'accounts/signup.html',{'form':form})

def login_user(request):
    if request.method == 'POST':
        form=forms.loginUserForm(data=request.POST)
        if form.is_valid():
            try:
                user=form.get_user()
                login(request,user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return render(request,'accounts/personal.html',{'form':form})
            except:
                pass
        else:
            return render(request,'accounts/signup.html',{'form':form})
    else:
        form=forms.loginUserForm()
    return render(request,'accounts/login.html',{'form':form})

#login customerForm

def is_customer(user1):
    try:
        customer=models.Customer.objects.get(user=user1)
        return True
    except :
        return False


#does customer exist
def afterlogin_view(request):
    if request.user.is_staff:
        return redirect('accounts:showadminprofile')
    elif is_customer(request.user):
        return redirect('accounts:customerhome')
    else:
        return redirect('accounts:showadminprofile')
        # return redirect('pompsale:listp')


def logout_user(request):
    if request.method== 'POST':
        logout(request)
        return redirect('accounts:customerlogin')

def show(request):
    if request.method=='POST':
        form=ShowForm(request.POST)
        if form.is_valid():
            pass
    else:
        form=ShowForm()
    return form
#customer form
def customer_signup_view(request):
    userform=forms.createUserCustomer()
    customerform=forms.customerPersonalForm()
    mydict={'userForm':userform,'customerForm':customerform}
    if request.method == 'POST':
        userform=forms.createUserCustomer(request.POST)
        customerform=forms.customerPersonalForm(request.POST,request.FILES)
        if userform.is_valid() and customerform.is_valid() :
            user=userform.save()
            user.set_password(user.password)
            user.save()
            customer=customerform.save(commit=False)
            customer.user=user
            customer.isbuyer=True
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            return HttpResponseRedirect('customerlogin')
    return render(request,'accounts/customersignup.html',context=mydict)
#homepage customer
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    #get model another app
    model=apps.get_model('pomp','pomps')
    pompten=model.objects.all()[:10]
    return render(request,'accounts/personal.html',{'pomps':pompten})

@login_required(login_url='customerlogin')
def admin_baner_view(request):
    return render(request,'accounts/adminbaner.html')

#view customer profile
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer=models.Customer.objects.get(user=request.user)
    return render(request,'accounts/showcustomerprofile.html',{'customer':customer})

#edit customer profile
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_edit(request):
    activeuser=models.User.objects.get(id=request.user.id)
    customer=models.Customer.objects.get(user_id=request.user.id)
    userForm=forms.createUserCustomer(instance=activeuser)
    customerForm=forms.customerPersonalForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.createUserCustomer(request.POST,instance=activeuser)
        customerForm=forms.customerPersonalForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('accounts:customerlogin')
    return render(request,'accounts/editcustomerprofile.html',context=mydict)
#admin functions
#admin homepage
@login_required(login_url='customerlogin')
def admin_home_view(request):
    user=models.User.objects.get(id=request.user.id)
    return render(request,'accounts/showadminprofile.html',{'adminuser':user})
#edit admin profile
@login_required(login_url='customerlogin')
def admin_edit_profile(request):
    activeuser=models.User.objects.get(id=request.user.id)
    userForm=forms.createUserCustomer(instance=activeuser)
    mydict={'userForm':userForm}
    if request.method=='POST':
        userForm=forms.createUserCustomer(request.POST,instance=activeuser)
        if userForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            return redirect('accounts:customerlogin')
    return render(request,'accounts/editadminprofile.html',context=mydict)
#show all customer by admin
@login_required(login_url='customerlogin')
def show_all_customer(request):
    customers=models.Customer.objects.all()
    return render(request,'accounts/allcustomers.html',{'customers':customers})
#delete customer by admin
@login_required(login_url='customerlogin')
def delete_special_customer(request,ck):
    customer=models.Customer.objects.get(id=ck)
    customer.delete()
    customers=models.Customer.objects.all()
    return render(request,'accounts/allcustomers.html',{'customers':customers})
