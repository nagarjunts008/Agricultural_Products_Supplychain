from django.conf.urls import url, include
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

# *********************************
    path('manufacturerloginpage',views.manufacturerloginpage,name='manufacturerloginpage'),
    path('manufacturerlogin',views.manufacturerlogin,name='manufacturerlogin'),

    path('manufacturerlogout',views.manufacturerlogout,name='manufacturerlogout'),

    path('manufacturerhome',views.manufacturerhome,name='manufacturerhome'),

    path('manufacturersignuppage',views.manufacturersignuppage,name='manufacturersignuppage'),
    path('manufacturersignup',views.manufacturersignup,name='manufacturersignup'),
    path('manufacturercheckotp',views.manufacturercheckotp,name='manufacturercheckotp'),
    path('manufacturerresendotp',views.manufacturerresendotp,name='manufacturerresendotp'),

    path('manufactureraddproductpage',views.manufactureraddproductpage,name='manufactureraddproductpage'),
    path('manufactureraddproduct',views.manufactureraddproduct,name='manufactureraddproduct'),

    path('manufacturerviewproductspage',views.manufacturerviewproductspage,name='manufacturerviewproductspage'),

    path('manufacturervieworders',views.manufacturervieworders,name='manufacturervieworders'),
    path('manufacture_dispatch_page', views.manufacture_dispatch_page, name='manufacture_dispatch_page'),

    path('manufacturerordercancelledlist',views.manufacturerordercancelledlist,name='manufacturerordercancelledlist'),

    path('manufacturerdispatcher', views.manufacturerdispatcher, name='manufacturerdispatcher'),
    
    path('manufacturerdispatchedorderslist', views.manufacturerdispatchedorderslist, name='manufacturerdispatchedorderslist'),



# *************************************** User **************************************
    path('',views.userloginpage,name='userloginpage'),
    path('userlogin',views.userlogin,name='userlogin'),

    path('userlogout',views.userlogout,name='userlogout'),

    path('userhomepage',views.userhomepage,name='userhomepage'),

    path('usersignuppage',views.usersignuppage,name='usersignuppage'),
    path('usersignup',views.usersignup,name='usersignup'),
    path('usercheckotp',views.usercheckotp,name='usercheckotp'),
    path('userresendotp',views.userresendotp,name='userresendotp'),

    path('userviewproductspage',views.userviewproductspage,name='userviewproductspage'),

    path('userplaceorder',views.userplaceorder,name='userplaceorder'),
    path('usercancelorder',views.usercancelorder,name='usercancelorder'),

    path('userordercancelledlist',views.userordercancelledlist,name='userordercancelledlist'),

    path('orderplaced',views.orderplaced,name='orderplaced'),

    path('userordertrackinglist',views.userordertrackinglist,name='userordertrackinglist'),
    path('userbacktrack',views.userbacktrack,name='userbacktrack'),

    path('userorderdeliverdlist',views.userorderdeliverdlist,name='userorderdeliverdlist'),



# ************************************ Logistics ***********************************
    path('logisticsloginpage',views.logisticsloginpage,name='logisticsloginpage'),
    path('logisticslogin',views.logisticslogin,name='logisticslogin'),

    path('logisticslogout',views.logisticslogout,name='logisticslogout'),
    
    path('logisticssignuppage',views.logisticssignuppage,name='logisticssignuppage'),
    path('logisticssignup',views.logisticssignup,name='logisticssignup'),
    path('logisticscheckotp',views.logisticscheckotp,name='logisticscheckotp'),
    path('logisticsresendotp',views.logisticsresendotp,name='logisticsresendotp'),

    path('logisticshomepage',views.logisticshomepage,name='logisticshomepage'),

    path('logisticspendingdelivary',views.logisticspendingdelivary,name='logisticspendingdelivary'),
    path('logistics_view_user_info_page',views.logistics_view_user_info_page,name='logistics_view_user_info_page'),
    path('logistics_dispatch_page',views.logistics_dispatch_page,name='logistics_dispatch_page'),
    path('logisticsdispatcher',views.logisticsdispatcher,name='logisticsdispatcher'),

    path('logistics_dispatch_user_page',views.logistics_dispatch_user_page,name='logistics_dispatch_user_page'),
    path('logisticsdispatcheruser',views.logisticsdispatcheruser,name='logisticsdispatcheruser'),
    path('logisticscompleteddelivary',views.logisticscompleteddelivary,name='logisticscompleteddelivary'),

    path('logisticsdelivaredlist',views.logisticsdelivaredlist,name='logisticsdelivaredlist'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)