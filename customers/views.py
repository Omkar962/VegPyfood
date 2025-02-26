from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User,UserProfile
from accounts.forms import UserProfileForm,UserInfoForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from orders.models import Order,OrderedFood
import simplejson as json

@login_required(login_url='login')
def cprofile(req):
    profile=get_object_or_404(UserProfile,user=req.user)
    
    if req.method=="POST":
        profile_form=UserProfileForm(req.POST,req.FILES,instance=profile)
        user_form=UserInfoForm(req.POST,instance=req.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()

            messages.success(req,'Profile updated')
            return redirect('cprofile')
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        profile_form=UserProfileForm(instance=profile)
        user_form=UserInfoForm(instance=req.user)



    context={
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile
    }


    return render(req,'customers/cprofile.html',context)

@login_required(login_url='login')
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders,
    }
    return render(request,"customers/my_orders.html",context)


@login_required(login_url='login')
def order_detail(request,order_number):
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_food=OrderedFood.objects.filter(order=order)
        subtotal=0
        for i in ordered_food:
            subtotal+=(i.price*i.quantity)
        tax_data=json.loads(order.tax_data)

        context={
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':subtotal,
            'tax_data':tax_data
        }
        return render(request,"customers/order_detail.html",context)
    except:
        return redirect('customer')

    


