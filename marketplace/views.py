from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from .context_processors import cart_counter
from vendor.models import Vendor
from menu.models import Category,Fooditem
from django.db.models import Prefetch
from .models import Cart

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
    if req.user.is_authenticated:
       cart_items=Cart.objects.filter(user=req.user)
    else:
        cart_items=None
    context={'vendor':vendor,'categories':categories,'cart_items':cart_items}
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
                    return JsonResponse({'status':'success','message':'Increased cart quantity','cart_counter':cart_counter(req),'qty':checkCart.quantity})
                except:
                    checkCart=Cart.objects.create(user=req.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'success','message':'Added to cart','cart_counter':cart_counter(req),'qty':checkCart.quantity})
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
                    return JsonResponse({'status':'Success','cart_counter':cart_counter(req),'qty':checkCart.quantity})
                except:
                    return JsonResponse({'status':'Failed','message':'Fooditem not present in cart'})
            except:
                return JsonResponse({'status':'Failed','message':'This fooditem does not exists!'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})

    return JsonResponse({'status':'login_required','message':'You need to login to add to cart'})