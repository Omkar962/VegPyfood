from vendor.models import Vendor


def get_vendor(request):
    """
    Get the vendor object for the logged-in user.
    """
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return {'vendor': vendor}