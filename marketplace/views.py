from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404,redirect
from .context_processors import cart_counter,get_cart_amount
from vendor.models import Vendor,OpeningHour
from menu.models import Category,Fooditem
from django.db.models import Prefetch
from .models import Cart
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from datetime import date,datetime
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

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
    
    opening_hours=OpeningHour.objects.filter(vendor=vendor).order_by('day','from_hour')

    today_date=date.today()
    today=today_date.isoweekday()
    current_opening_hours=OpeningHour.objects.filter(vendor=vendor,day=today)

    if req.user.is_authenticated:
       cart_items=Cart.objects.filter(user=req.user)
    else:
        cart_items=None
    context={
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
        'opening_hours':opening_hours,
        'current_opening_hours':current_opening_hours,
    }
    return render(req,'marketplace/vendor_detail.html',context)



def add_to_cart(req,fooditem_id):
    if req.user.is_authenticated:
        if req.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the fooditem exists
            try:
                fooditem=Fooditem.objects.get(id=fooditem_id)
                # check if the fooditem is already adeed to cart
                try:
                    checkCart=Cart.objects.get(user=req.user,fooditem=fooditem)
                    checkCart.quantity+=1
                    checkCart.save()
                    return JsonResponse({'status':'success','message':'Increased cart quantity','cart_counter':cart_counter(req),'qty':checkCart.quantity,'cart_amount':get_cart_amount(req)})
                except:
                    checkCart=Cart.objects.create(user=req.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'success','message':'Added to cart','cart_counter':cart_counter(req),'qty':checkCart.quantity,'cart_amount':get_cart_amount(req)})
            except:
                return JsonResponse({'status':'failed','message':'This fooditem does not exists!'})
        else:
            return JsonResponse({'status':'failed','message':'Invalid request'})

    return JsonResponse({'status':'login_required','message':'You need to login to add to cart'})
    


def decrease_cart(req,fooditem_id):
    if req.user.is_authenticated:
        if req.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the fooditem exists
            try:
                fooditem=Fooditem.objects.get(id=fooditem_id)
                # check if the fooditem is already adeed to cart
                try:
                    checkCart=Cart.objects.get(user=req.user,fooditem=fooditem)
                    if checkCart.quantity>1:
                        checkCart.quantity-=1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity=0
                    return JsonResponse({'status':'Success','cart_counter':cart_counter(req),'qty':checkCart.quantity,'cart_amount':get_cart_amount(req)})
                except:
                    return JsonResponse({'status':'Failed','message':'Fooditem not present in cart'})
            except:
                return JsonResponse({'status':'Failed','message':'This fooditem does not exists!'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})

    return JsonResponse({'status':'login_required','message':'You need to login to add to cart'})


@login_required(login_url='login')
def cart(req):
    cart_items=Cart.objects.filter(user=req.user).order_by('created_at')
    context={
        'cart_items':cart_items
    }
    
    return render(req,'marketplace/cart.html',context)


def delete_cart(req,cart_id):
    if req.user.is_authenticated:
        if req.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item=Cart.objects.get(user=req.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success','message':'Cart item has been deleted!','cart_counter':cart_counter(req),'cart_amount':get_cart_amount(req)})
            except:
                return JsonResponse({'status':'Failed','message':'Cart item does not exist!'})
        else:
             return JsonResponse({'status':'Failed','message':'Invalid request'})
        


def search(req):
    if not 'address' in req.GET:
        return redirect('marketplace')
    address=req.GET['address']
    latitude=req.GET['lat']
    longitude=req.GET['lng']
    radius=req.GET['radius']
    keyword=req.GET['keyword']

    # Get vendors based on food items matching the keyword
    fetch_vendors_by_fooditem=Fooditem.objects.filter(food_title__icontains=keyword,is_available=True).values_list('vendor',flat=True)

    # Combining food search based vendors filter and  simple keyword matching vendors filters
    vendors=Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditem)|Q(vendor_name__icontains=keyword,is_approved=True,user__is_active=True))
    
    if latitude and longitude and radius:
        pnt=GEOSGeometry('POINT(%s %s)'% (longitude,latitude))
        vendors=Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditem)|Q(vendor_name__icontains=keyword,is_approved=True,user__is_active=True),
                                      user_profile__location__distance_lte=(pnt,D(km=radius))
                                      ).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance")
        for v in vendors:
            v.kms=round(v.distance.km,1)

    vendor_Count=vendors.count()
    context={
        'vendors':vendors,
        'vendor_Count':vendor_Count,
        'source_location':address
    }

    return render(req,'marketplace/listings.html',context)


