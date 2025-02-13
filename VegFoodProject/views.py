from django.shortcuts import render
from vendor.models import Vendor


def home(req):
    vendors=Vendor.objects.filter(user__is_active=True,is_approved=True)[:8]
    context={'vendors':vendors}
    return render(req,'home.html',context)

