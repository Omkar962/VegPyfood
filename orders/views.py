from django.shortcuts import render,redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amount
from . forms import OrderForm
import simplejson as json
from .models import Order
from .utils import generate_order_number

def place_order(req):
    cart_items=Cart.objects.filter(user=req.user).order_by("created_at")
    cart_count=cart_items.count()

    if cart_count<=0:
        return redirect('marketplace')
    
    subtotal=get_cart_amount(req)['subtotal']
    total_tax=get_cart_amount(req)['tax']
    total=get_cart_amount(req)['total']
    tax_data=get_cart_amount(req)['tax_dict']


    if req.method=="POST":
        form=OrderForm(req.POST)
        if form.is_valid():
            order=Order()
            order.first_name=form.cleaned_data['first_name']
            order.last_name=form.cleaned_data['last_name']
            order.phone=form.cleaned_data['phone']
            order.email=form.cleaned_data['email']
            order.address=form.cleaned_data['address']
            order.country=form.cleaned_data['country']
            order.state=form.cleaned_data['state']
            order.city=form.cleaned_data['city']
            order.pin_code=form.cleaned_data['pin_code']
            order.user=req.user
            order.total=total
            order.tax_data=json.dumps(tax_data)
            order.total_tax=total_tax
            order.payment_method=req.POST['payment_method']
            order.save()
            order.order_number=generate_order_number(order.id)
            order.save()

            return redirect('place_order')


        else:
            print(form.errors)

    return render(req,'orders/place_order.html')