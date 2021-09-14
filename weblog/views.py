from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.apps import apps
import accounts
# def about(request):
#     return HttpResponse("HelloWorld")
#
# def home(request):
#     return HttpResponse("Home Page")


def about(request):
    if accounts.views.is_customer(request.user):
        return render(request,'about.html',{'key':'2'})
    else:
        return render(request,'about.html',{'key':'1'})
    return render(request,'about.html',{'key':'0'})
def home(request):
    key=''
    if accounts.views.is_customer(request.user):
        key='2'
    else:
        key='1'

    model=apps.get_model('pomp','pomps')
    pompten=model.objects.all()[:10]
    mydict={'pomps':pompten,'key':key}
    return render(request,'index.html',context=mydict)

def contact(request):
    if accounts.views.is_customer(request.user):
        return render(request,'contact.html',{'key':'2'})
    else:
        return render(request,'contact.html',{'key':'1'})
    return render(request,'contact.html',{'key':'0'})
