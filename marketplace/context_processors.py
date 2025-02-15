from .models import Cart
from menu.models import Fooditem


def cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for item in cart_items:
                    cart_count += item.quantity
        except:
            cart_count = 0
    else:
        cart_count = 0
    return {'cart_count': cart_count}


def get_cart_amount(request):
    subtotal=0
    tax=0
    total=0
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        for i in cart_items:
            fooditem=Fooditem.objects.get(pk=i.fooditem.id)
            subtotal+=(fooditem.price*i.quantity)
        
        total=subtotal+tax
    return {'subtotal':subtotal,'tax':tax,'total':total}