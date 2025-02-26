from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from menu.models import Category
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from vendor.forms import VendorForm,OpeningHourForm
from vendor.models import Vendor,OpeningHour
from django.contrib import messages
from menu.models import Fooditem
from django.contrib.auth.decorators import login_required,user_passes_test
from menu.forms import CategoryForm, FooditemForm
from django.template.defaultfilters import slugify
from orders.models import Order,OrderedFood

def get_vendor(request):
    return Vendor.objects.get(user=request.user)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    vendor=get_object_or_404(Vendor,user=request.user)

    if request.method=='POST':
        profile_form=UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form=VendorForm(request.POST,request.FILES,instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect('vprofile')
    else:
        profile_form=UserProfileForm(instance=profile)
        vendor_form=VendorForm(instance=vendor)

    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor
    }
    return render(request,'vendor/vprofile.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_Builder(request):
    vendor=get_vendor(request)
    categories=Category.objects.filter(vendor=vendor)
    context={
        'categories':categories
    }
    return render(request,'vendor/menu-builder.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditem_by_category(request,pk=None):
    vendor=get_vendor(request)
    category=get_object_or_404(Category,pk=pk)
    fooditems=Fooditem.objects.filter(vendor=vendor,category=category)
    context={
        'category':category,
        'fooditems':fooditems
    }
    return render(request,'vendor/fooditem_by_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.save()
            category.slug=slugify(category_name)+'-'+str(category.id)
            category.save()
            
            messages.success(request,'Category Added Successfully')
            return redirect('menu_Builder')
    else:
        form=CategoryForm()
    context={
        'form':form
    }
    return render(request,'vendor/add_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)

    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)
            category.save()
            messages.success(request,'Category Updated Successfully')
            return redirect('menu_Builder')
    else:
        form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category
    }
    return render(request,'vendor/edit_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category Deleted Successfully')
    return redirect('menu_Builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_fooditem(request):
    if request.method=='POST':
        form=FooditemForm(request.POST,request.FILES)
        if form.is_valid():
            foodtitle=form.cleaned_data['food_title']
            fooditem=form.save(commit=False)
            fooditem.vendor=get_vendor(request)
            fooditem.slug=slugify(foodtitle)
            fooditem.save()
            messages.success(request,'Food Item Added Successfully')
            return redirect('fooditem_by_category',fooditem.category.id)
    else:

        form=FooditemForm()
        form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context={
        'form':form
    }
    return render(request,'vendor/add_fooditem.html',context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_fooditem(request,pk=None):
    fooditem=get_object_or_404(Fooditem,pk=pk)

    if request.method=='POST':
        form=FooditemForm(request.POST,instance=fooditem)
        if form.is_valid():
            foodtitle=form.cleaned_data['food_title']
            fooditem=form.save(commit=False)
            fooditem.vendor=get_vendor(request)
            fooditem.slug=slugify(foodtitle)
            fooditem.save()
            messages.success(request,'Food Item Updated Successfully')
            return redirect('fooditem_by_category',fooditem.category.id)
    else:
        form=FooditemForm(instance=fooditem)
        form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context={
        'form':form,
        'fooditem':fooditem
    }
    return render(request,'vendor/edit_fooditem.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_fooditem(request,pk=None):
    fooditem=get_object_or_404(Fooditem,pk=pk)
    fooditem.delete()
    messages.success(request,'Food Item Deleted Successfully')
    return redirect('fooditem_by_category',fooditem.category.id)


def opening_hours(req):
    opening_hours=OpeningHour.objects.filter(vendor=get_vendor(req))
    form=OpeningHourForm()
    context={
        'form':form,
        'opening_hours':opening_hours
    }
    return render(req,'vendor/opening_hours.html',context)

def add_opening_hours(req):
    if req.user.is_authenticated:
        if req.headers.get('x-requested-with') == 'XMLHttpRequest' and req.method=='POST':
            day=req.POST.get('day')
            from_hour=req.POST.get('from_hour')
            to_hour=req.POST.get('to_hour')
            is_closed=req.POST.get('is_closed')
            try:
                hour=OpeningHour.objects.create(vendor=get_vendor(req),day=day,from_hour=from_hour,to_hour=to_hour,is_closed=is_closed)
                if hour:
                    day=OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response={'status':'success','id':hour.id,'day':day.get_day_display(),'is_closed':'Closed'}
                    else:
                        response={'status':'success','id':hour.id,'day':day.get_day_display(),'from_hour':from_hour,'to_hour':to_hour}
                return JsonResponse(response)
            except IntegrityError as e:
                response={'status':'failed','message':from_hour+'-'+to_hour+' already exists for this day!','error':str(e)}
                return JsonResponse(response)
        else:
            HttpResponse("Invalid Request")


def remove_opening_hours(req,pk=None):
    if req.user.is_authenticated:
        if req.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour=get_object_or_404(OpeningHour,pk=pk)
            hour.delete()
            return JsonResponse({'status':'success','id':pk})

def order_detail(req,order_number):
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_food=OrderedFood.objects.filter(order=order,fooditem__vendor=get_vendor(req))

        context={
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':order.get_total_by_vendor()['subtotal'],
            'tax_data':order.get_total_by_vendor()['tax_dict'],
            'total':order.get_total_by_vendor()['total']
        }
        return render(req,'vendor/order_detail.html',context)
    except:
        return redirect('vendor')
    

def my_orders(request):
    vendor=Vendor.objects.get(user=request.user)
    orders=Order.objects.filter(vendors__in=[vendor.id],is_ordered=True).order_by('-created_at')
    context={
        'orders':orders,
    }
    return render(request,'vendor/my_orders.html',context)
  