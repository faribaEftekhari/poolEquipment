from django.urls import path
from . import views
app_name="pompsale"
urlpatterns=[
path('',views.pomplist,name='listp'),
path('create',views.create_pomp,name="create"),
path('search',views.search_view,name='search'),
path('order/<int:idkey>',views.order_register,name='order'),
path('orderedproducts',views.ordered_product,name='orderedproducts'),
path('deleteorder/<int:pk>',views.delete_ordered_product,name='deleteorder'),
path('showallproduct',views.show_all_procuct,name='showallproduct'),
path('deleteproduct/<int:pk>',views.delete_product,name='deleteproduct'),
path('allorderedproducts',views.all_ordered_product,name='allorderedproducts'),
path('customerordereds/<int:ck>',views.show_all_customer_ordered,name='customerordereds'),
path('deletecustomordered/<int:pk>',views.delete_customer_ordered,name='deletecustomordered'),
path('<slugg>',views.pompdetail,name='detalp'),
]
