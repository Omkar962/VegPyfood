from .models import Cart,Tax
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
    tax_dict={}
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        for i in cart_items:
            fooditem=Fooditem.objects.get(pk=i.fooditem.id)
            subtotal+=(fooditem.price*i.quantity)

        get_tax=Tax.objects.filter(is_active=True)

        for i in get_tax:
            taxt_type=i.tax_type
            tax_percentage=i.tax_percentage

            tax_amount=round((tax_percentage*subtotal)/100,2)
            tax_dict.update({taxt_type:{str(tax_percentage):tax_amount}})

        for k in tax_dict.values():
            for x in k.values():
                tax=tax+x

        total=subtotal+tax
    return {'subtotal':subtotal,'tax':tax,'total':total,'tax_dict':tax_dict}