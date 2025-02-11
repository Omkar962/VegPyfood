from django.shortcuts import get_object_or_404, redirect, render

from menu.models import Category
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from vendor.forms import VendorForm
from vendor.models import Vendor
from django.contrib import messages
from menu.models import Fooditem
from django.contrib.auth.decorators import login_required,user_passes_test
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify

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


def add_category(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)
            category.save()
            messages.success(request,'Category Added Successfully')
            return redirect('menu_Builder')
    else:
        form=CategoryForm()
    context={
        'form':form
    }
    return render(request,'vendor/add_category.html',context)

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


def delete_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category Deleted Successfully')
    return redirect('menu_Builder')