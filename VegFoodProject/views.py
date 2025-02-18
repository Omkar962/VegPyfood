from django.shortcuts import render
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

def get_or_set_Curr_location(req):
    if 'lat' in req.session:
        lat=req.session['lat']
        lng=req.session['lng']
        return lng,lat
    
    elif 'lat' in req.GET:
        lat=req.GET.get('lat')
        lng=req.GET.get('lng')
        req.session['lat']=lat
        req.session['lng']=lng
        return lng,lat
    
    else:
        return None
    
def home(req):
    if get_or_set_Curr_location(req) is not None:

        pnt=GEOSGeometry('POINT(%s %s)'% (get_or_set_Curr_location(req)))

        vendors=Vendor.objects.filter(user_profile__location__distance_lte=(pnt,D(km=125))).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance")
        for v in vendors:
            v.kms=round(v.distance.km,1)
    else:
        vendors=Vendor.objects.filter(user__is_active=True,is_approved=True)[:8]
    context={'vendors':vendors}
    return render(req,'home.html',context)

