from django.shortcuts import render,get_object_or_404
from vendor.models import Vendor
from menu.models import Category,Fooditem
from django.db.models import Prefetch

def marketplace(req):
    vendors=Vendor.objects.filter(user__is_active=True,is_approved=True)
    vendor_Count=vendors.count()
    context={'vendors':vendors,'vendor_Count':vendor_Count}
    return render(req,'marketplace/listings.html',context)

def vendor_detail(req,vendor_slug):
    vendor=get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories=Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=Fooditem.objects.filter(is_available=True),
            ))
    context={'vendor':vendor,'categories':categories}
    return render(req,'marketplace/vendor_detail.html',context)