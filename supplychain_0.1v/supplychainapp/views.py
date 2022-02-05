from django.shortcuts import render, redirect, HttpResponse
from . models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
import re
import csv, io
import math, random
import pandas as pd
from django.http import JsonResponse

# from django.core.context_processors import csrf
# from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context,RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse


# Create your views here.
def listToString(s):
    str1 = " " 
    return (str1.join(s)) 

def manufacturerloginpage(request):
    return render(request,'manufacturerlogin.html')

def manufacturerhome(request):
    mid = request.session['mid']
    m = manufacturer.objects.get(id=mid)
    return render(request,'manufacturerhome.html',{'mname':m.manufacturername})

def manufacturerlogout(request):
    request.session['mid'] = None
    return render(request,'manufacturerlogin.html')

def manufacturerlogin(request):
    if request.method=='POST':
        mail = request.POST['email']
        pwd = request.POST['password']

        try:
            m = manufacturer.objects.get(email=mail, password=pwd)
            request.session['mid'] = m.id
            print(m.id,m.manufacturername)
            return render(request, 'manufacturerhome.html',{'mname':m.manufacturername})

        except ObjectDoesNotExist:
            # lid = None
            request.session['mid'] = None
            messages.info(request,'Invalid credentials')
            return redirect('manufacturerloginpage')
         
    return redirect('manufacturerloginpage')

    
def manufacturersignuppage(request):
    return render(request,'manufacturersignup.html')

def manufacturersignup(request):
    if request.method=='POST':
        name = request.POST['name']
        cname = request.POST['companyname']
        mail = request.POST['email']
        ph = request.POST['phone']
        add = request.POST['address']
        state = request.POST['state']
        country = request.POST['country']
        pwd = request.POST['password']
        cpwd = request.POST['cpassword']

        try:
            if cpwd == pwd:
                mx = {'manufacturername':name,'companyname':cname,'email':mail,'phone':ph,'address':add,'state':state,'country':country,'password':pwd}
                request.session['manufacturerverification'] = mx


                digits = "0123456789"
                OTP = ""
                for i in range(4):
                    OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
                request.session['otp'] = OTP

                text = []
                text.append(OTP)
                text.append(" This is Your OTP and Please Don't share this with others ")

                Subject = "Agriculture Products Supplychain-OTP"
                Main_Text = listToString(text)
                From_mail = settings.EMAIL_HOST_USER
                To_mail = [mail]

                send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
                messages.info(request,'OTP is sent to Gmail')

                return render(request,'manufacturerotp.html')
            else:
                messages.info(request,'Confirm Password does not Match')

        except ObjectDoesNotExist:
            m = manufacturer.objects.get(email=mail)
            messages.info(request,'Email Address already Taken')
            return redirect('index')

            

    return redirect('manufacturerloginpage')

def manufacturercheckotp(request):
    if request.method=='POST':
        mail_otp = request.POST['otpinput']
        mx = request.session['manufacturerverification']
        OTP = request.session['otp']
        if mail_otp == OTP:
            manufacturersignup = manufacturer(manufacturername=mx['manufacturername'],companyname=mx['companyname'],email=mx['email'],phone=mx['phone'],address=mx['address'],state=mx['state'],country=mx['country'],password=mx['password'])
            manufacturersignup.save()
            messages.info(request,'Successfully Registered')
            return redirect('manufacturerloginpage')
        else:
            messages.info(request,'Something Went Wrong')
            return redirect('manufacturerloginpage')
        
def manufacturerresendotp(request):
    mx = request.session['manufacturerverification']

    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    print(OTP)
    request.session['otp'] = OTP
    
    text = []
    text.append(OTP)
    text.append(" This is Your OTP and Please Don't share this with others ")

    Subject = "Agriculture Products Supplychain-OTP"
    Main_Text = listToString(text)
    From_mail = settings.EMAIL_HOST_USER
    To_mail = [mx['email']]

    send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
    messages.info(request,'OTP is sent to Gmail')

    return render(request,'manufacturerotp.html')


def manufactureraddproductpage(request):
    return render(request, 'manufactureraddproduct.html')

def manufactureraddproduct(request):
    if request.method == 'POST':
        pname = request.POST['pname']
        price = request.POST['price']
        description = request.POST['description']
        category = request.POST['category']
        img = request.FILES['image']
        mid = request.session['mid'] 
        
        try:
            addedproducts = products(manufacturerid=mid,productname=pname,price=price,img=img,category=category,description=description)
            addedproducts.save()
            messages.info(request,'Added Successfully')
        except:
            print("Something went wrong")
            messages.info(request,'Something went wrong')
            return render(request, 'manufacturerhome.html')

    return render(request, 'manufactureraddproduct.html')

def manufacturerviewproductspage(request):
    mid = request.session['mid']
    product = products.objects.filter(manufacturerid=mid)
    return render(request, 'manufacturerviewproducts.html',{'pro':product})

def manufacturervieworders(request):
    mid = request.session['mid']
    product = products.objects.filter(manufacturerid=mid)
    return render(request, 'manufacturervieworders.html',{'pro':product,'mid':mid})
    
def manufacture_dispatch_page(request):
    mid = request.session['mid']
    product = products.objects.filter(manufacturerid=mid)
    logistic = logistics.objects.all()
    return render(request, 'manufacturerdispatch.html',{'pro':product,'mid':mid,'logistic':logistic})

def manufacturerordercancelledlist(request):
    mid = request.session['mid']
    product = products.objects.filter(manufacturerid=mid)
    return render(request, 'manufacturerordercancelledlist.html',{'pro':product,'mid':mid})

def manufacturerdispatcher(request):
    if request.method=='POST':
        userid = request.POST['userid']
        orderid = request.POST['orderid']
        productid = request.POST['productid']
        manufacturerid = request.POST['manufacturerid']
        trasactionhash = request.POST['thash']
        orderstatus = request.POST['orderstatus']
        print(userid, orderid, productid, manufacturerid, trasactionhash)
        placeordersave = ordertrack(userid=userid,orderid=orderid,productid=productid,manufacturerid=manufacturerid,orderstatus=orderstatus,trasactionhash=trasactionhash)
        placeordersave.save()
        messages.info(request,'Product Order Dispatched Successfully')
        return redirect('manufacturerhome')

def manufacturerdispatchedorderslist(request):
    mid = request.session['mid']
    product = products.objects.filter(manufacturerid=mid)
    return render(request, 'manufacturerdispatchedorderslist.html',{'pro':product,'mid':mid})

# **************************************** User ***************************************************
def userloginpage(request):
    return render(request, 'userlogin.html')

def userhomepage(request):
    uid = request.session['uid']
    u = user.objects.get(id=uid)
    return render(request, 'userhome.html', {'uname':u.username})

def userlogout(request):
    request.session['uid'] = None
    return redirect('userloginpage')

def userlogin(request):
    if request.method=='POST':
        mail = request.POST['email']
        pwd = request.POST['password']

        try:
            u = user.objects.get(email=mail, password=pwd)
            request.session['uid'] = u.id
            print(u.id,u.username)
            return render(request, 'userhome.html',{'uname':u.username})

        except ObjectDoesNotExist:
            # uid = None
            request.session['uid'] = None
            messages.info(request,'Invalid credentials')
            return redirect('userloginpage')
         
    return redirect('userloginpage')

def usersignuppage(request):
    return render(request, 'usersignup.html')

def usersignup(request):
    if request.method=='POST':
        name = request.POST['name']
        mail = request.POST['email']
        ph = request.POST['phone']
        add = request.POST['address']
        pcode = request.POST['pincode']
        state = request.POST['state']
        country = request.POST['country']
        pwd = request.POST['password']
        cpwd = request.POST['cpassword']

        try:
            u = user.objects.get(email=mail)
            messages.info(request,'Email Address already Taken')
            return redirect('index')

        except ObjectDoesNotExist:
            if cpwd == pwd:
                ux = {'username':name,'email':mail,'phone':ph,'address':add,'pincode':pcode,'state':state,'country':country,'password':pwd}
                request.session['userverification'] = ux


                digits = "0123456789"
                OTP = ""
                for i in range(4):
                    OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
                request.session['otp'] = OTP

                text = []
                text.append(OTP)
                text.append(" This is the OTP to recieve your order. Please Share the OTP with the delivery partner. ")

                Subject = "Agriculture Products Supplychain-OTP"
                Main_Text = listToString(text)
                From_mail = settings.EMAIL_HOST_USER
                To_mail = [mail]

                send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
                messages.info(request,'OTP is sent to Gmail')

                return render(request,'userotp.html')
            else:
                messages.info(request,'Confirm Password does not Match')

    return redirect('/')

def usercheckotp(request):
    if request.method=='POST':
        mail_otp = request.POST['otpinput']
        ux = request.session['userverification']
        OTP = request.session['otp']
        if mail_otp == OTP:
            usersignup = user(username=ux['username'],email=ux['email'],phone=ux['phone'],address=ux['address'],pincode=ux['pincode'],state=ux['state'],country=ux['country'],password=ux['password'])
            usersignup.save()
            messages.info(request,'Successfully Registered')
            return redirect('/')
        else:
            messages.info(request,'Something Went Wrong')
            return redirect('/')
        
def userresendotp(request):
    ux = request.session['userverification']

    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    print(OTP)
    request.session['otp'] = OTP
    
    text = []
    text.append(OTP)
    text.append(" This is Your OTP and Please Don't share this with others ")

    Subject = "Agriculture Products Supplychain-OTP"
    Main_Text = listToString(text)
    From_mail = settings.EMAIL_HOST_USER
    To_mail = [ux['email']]

    send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
    messages.info(request,'OTP is sent to Gmail')

    return render(request,'userotp.html')

def userviewproductspage(request):
    uid = request.session['uid']
    product = products.objects.all()
    manufacturers = manufacturer.objects.all()
    u = user.objects.get(id=uid)
    return render(request, 'userviewproducts.html',{'pro':product,'man':manufacturers,'uid':uid,'u':u})

def orderplaced(request):
    uid = request.session['uid']
    product = products.objects.all()
    manufacturers = manufacturer.objects.all()
    u = user.objects.get(id=uid)
    return render(request, 'userorderplaced.html',{'pro':product,'man':manufacturers,'uid':uid,'u':u})

def userplaceorder(request):
    if request.method=='POST':
        userid = request.POST['userid']
        orderid = request.POST['orderid']
        productid = request.POST['productid']
        manufacturerid = request.POST['manufacturerid']
        trasactionhash = request.POST['thash']
        orderstatus = request.POST['orderstatus']
        
        print(userid, orderid, productid, manufacturerid, trasactionhash)
        placeordersave = ordertrack(userid=userid,orderid=orderid,productid=productid,manufacturerid=manufacturerid,orderstatus=orderstatus,trasactionhash=trasactionhash)
        placeordersave.save()

        messages.info(request,'Product Order Placed Successfully')

        return redirect('userhomepage')

def usercancelorder(request):
    if request.method=='POST':
        userid = request.POST['userid']
        orderid = request.POST['orderid']
        productid = request.POST['productid']
        manufacturerid = request.POST['manufacturerid']
        trasactionhash = request.POST['thash']
        orderstatus = request.POST['orderstatus']
        
        print(userid, orderid, productid, manufacturerid, trasactionhash, orderstatus)
        placeordersave = ordertrack(userid=userid,orderid=orderid,productid=productid,manufacturerid=manufacturerid,orderstatus=orderstatus,trasactionhash=trasactionhash)
        placeordersave.save()

        messages.info(request,'Product Order Cancelled Successfully')

        return redirect('userhomepage')

def userordercancelledlist(request):
    uid = request.session['uid']
    product = products.objects.all()
    manufacturers = manufacturer.objects.all()
    u = user.objects.get(id=uid)
    return render(request, 'userordercancelled.html',{'pro':product,'man':manufacturers,'uid':uid,'u':u})

def userordertrackinglist(request):
    uid = request.session['uid']
    product = products.objects.all()
    manufacturers = manufacturer.objects.all()
    u = user.objects.get(id=uid)
    return render(request, 'userordertracking.html',{'pro':product,'man':manufacturers,'uid':uid,'u':u})

def userbacktrack(request):
    if request.method=='POST':
        orderid = request.POST['orderid']
        oid = int(orderid)
        uid = request.session['uid']

        product = products.objects.all()
        manufacturers = manufacturer.objects.all()
        otracks = ordertrack.objects.filter(orderid=orderid).order_by('id')
        backtrack = ordertrack.objects.all()

        i = 0
        


        for o in backtrack:
            if o.orderid == oid:
                for p in product:
                    for m in manufacturers:
                        if p.id == o.productid and m.id == p.manufacturerid:
                            while i < 1:
                                print(p.productname,p.price,p.img,p.description,p.category,m.manufacturername)
                                ox = {'pname':p.productname,'pprice':p.price,'pimg':p.img,'pdesc':p.description,'pcat':p.category,'man':m.manufacturername}
                                i+=1
        
        return render(request, 'userbacktrack.html',{'orderid':orderid,'otracks':otracks,'ox':ox})

def userorderdeliverdlist(request):
    uid = request.session['uid']
    product = products.objects.all()
    manufacturers = manufacturer.objects.all()
    u = user.objects.get(id=uid)
    return render(request, 'userdeliverdcompletedlist.html',{'pro':product,'man':manufacturers,'uid':uid,'u':u})
# ******************************************* Logistics *******************************************
def logisticsloginpage(request):
    return render(request, 'logisticslogin.html')

def logisticshomepage(request):
    lid = request.session['lid']
    l = logistics.objects.get(id=lid)
    return render(request, 'logisticshome.html',{'lname':l.logisticsname})

def logisticslogout(request):
    request.session['lid'] = None
    return redirect('logisticslogin')

def logisticslogin(request):
    if request.method=='POST':
        mail = request.POST['email']
        pwd = request.POST['password']

        try:
            l = logistics.objects.get(email=mail, password=pwd)
            request.session['lid'] = l.id
            print(l.id,l.logisticsname)
            return render(request, 'logisticshome.html',{'lname':l.logisticsname})

        except ObjectDoesNotExist:
            # lid = None
            request.session['lid'] = None
            messages.info(request,'Invalid credentials')
            return redirect('logisticsloginpage')
         
    return redirect('logisticsloginpage')

def logisticssignuppage(request):
    return render(request, 'logisticssignup.html')

def logisticssignup(request):
    if request.method=='POST':
        name = request.POST['name']
        mail = request.POST['email']
        ph = request.POST['phone']
        add = request.POST['address']
        state = request.POST['state']
        country = request.POST['country']
        pwd = request.POST['password']
        cpwd = request.POST['cpassword']

        try:
            l = logistics.objects.get(email=mail)
            messages.info(request,'Email Address already Taken')
            return redirect('index')

        except ObjectDoesNotExist:
            if cpwd == pwd:
                lx = {'logisticsname':name,'email':mail,'phone':ph,'address':add,'state':state,'country':country,'password':pwd}
                request.session['logisticsverification'] = lx


                digits = "0123456789"
                OTP = ""
                for i in range(4):
                    OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
                request.session['otp'] = OTP

                text = []
                text.append(OTP)
                text.append(" This is Your OTP and Please Don't share this with others ")

                Subject = "Agriculture Products Supplychain-OTP"
                Main_Text = listToString(text)
                From_mail = settings.EMAIL_HOST_USER
                To_mail = [mail]

                send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
                messages.info(request,'OTP is sent to Gmail')

                return render(request,'logisticsotp.html')
            else:
                messages.info(request,'Confirm Password does not Match')

    return redirect('logisticsloginpage')

def logisticscheckotp(request):
    if request.method=='POST':
        mail_otp = request.POST['otpinput']
        lx = request.session['logisticsverification']
        OTP = request.session['otp']
        if mail_otp == OTP:
            logisticssignup = logistics(logisticsname=lx['logisticsname'],email=lx['email'],phone=lx['phone'],address=lx['address'],state=lx['state'],country=lx['country'],password=lx['password'])
            logisticssignup.save()
            messages.info(request,'Successfully Registered')
            return redirect('logisticsloginpage')
        else:
            messages.info(request,'Something Went Wrong')
            return redirect('logisticsloginpage')
        
def logisticsresendotp(request):
    lx = request.session['logisticsverification']

    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    print(OTP)
    request.session['otp'] = OTP
    
    text = []
    text.append(OTP)
    text.append(" This is Your OTP and Please Don't share this with others ")

    Subject = "Agriculture Products Supplychain-OTP"
    Main_Text = listToString(text)
    From_mail = settings.EMAIL_HOST_USER
    To_mail = [lx['email']]

    send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
    messages.info(request,'OTP is sent to Gmail')

    return render(request,'logisticsotp.html')

def logisticspendingdelivary(request):
    lid = request.session['lid']
    return render(request, 'logisticspendingdelivary.html',{'lid':lid})

def logistics_dispatch_page(request):
    lid = request.session['lid']
    logistic = logistics.objects.all()
    return render(request, 'logisticsdispatch.html',{'lid':lid,'logistic':logistic})

def logisticsdispatcher(request):
    if request.method=='POST':
        userid = request.POST['userid']
        orderid = request.POST['orderid']
        productid = request.POST['productid']
        manufacturerid = request.POST['manufacturerid']
        trasactionhash = request.POST['thash']
        orderstatus = request.POST['orderstatus']
        print(userid, orderid, productid, manufacturerid, trasactionhash)
        placeordersave = ordertrack(userid=userid,orderid=orderid,productid=productid,manufacturerid=manufacturerid,orderstatus=orderstatus,trasactionhash=trasactionhash)
        placeordersave.save()
        messages.info(request,'Product Order Dispatched to Others Successfully')
        return redirect('logisticshomepage')

def logistics_dispatch_user_page(request):
    lid = request.session['lid']
    logistic = logistics.objects.all()
    return render(request, 'logisticsdispatchuser.html',{'lid':lid,'logistic':logistic})

def logistics_view_user_info_page(request):
    if request.method=='POST':
        uid = request.session['uid']
        print(uid)
        userinfo = user.objects.get(id=uid)
    return render(request, 'logisticsviewuserinfopage.html',{'userinfo':userinfo})

def logisticsdispatcheruser(request):
    if request.method=='POST':
        lid = request.session['lid']
        fromaddress = request.POST['fromaddress']
        toaddress = request.POST['toaddress']
        userid = request.POST['userid']

        us = user.objects.get(id=userid)
        print(fromaddress, toaddress, userid,us.email)

        digits = "0123456789"
        OTP = ""
        for i in range(4):
            OTP += digits[math.floor(random.random() * 10)]
        print(OTP)
        request.session['otp'] = OTP

        text = []
        text.append(OTP)
        text.append(" This is Your OTP and Please Don't share this with others ")

        Subject = "Agriculture Products Supplychain-OTP"
        Main_Text = listToString(text)
        From_mail = settings.EMAIL_HOST_USER
        To_mail = [us.email]

        send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
        messages.info(request,'OTP is sent to Gmail')

        return render(request, 'logisticsdeliveredverification.html', {'lid':lid,'fromaddress':fromaddress,'toaddress':toaddress})


def logisticscompleteddelivary(request):
    if request.method=='POST':
        userid = request.POST['userid']
        orderid = request.POST['orderid']
        productid = request.POST['productid']
        manufacturerid = request.POST['manufacturerid']
        trasactionhash = request.POST['thash']
        orderstatus = request.POST['orderstatus']
        print(userid, orderid, productid, manufacturerid, trasactionhash)
        placeordersave = ordertrack(userid=userid,orderid=orderid,productid=productid,manufacturerid=manufacturerid,orderstatus=orderstatus,trasactionhash=trasactionhash)
        placeordersave.save()
        messages.info(request,'Product Order Dispatched to User Successfully')
        
    return redirect('logisticshomepage')

def logisticsdelivaredlist(request):
    lid = request.session['lid']
    return render(request, 'logisticsdelivaredlist.html',{'lid':lid})

