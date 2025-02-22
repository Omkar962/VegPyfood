from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User,UserProfile
from accounts.forms import UserProfileForm,UserInfoForm
from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required(login_url='login')
def cprofile(req):
    profile=get_object_or_404(UserProfile,user=req.user)
    
    if req.method=="POST":
        profile_form=UserProfileForm(req.POST,req.FILES,instance=profile)
        user_form=UserInfoForm(req.POST,instance=req.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()

            messages.success(req,'Profile updated')
            return redirect('cprofile')
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        profile_form=UserProfileForm(instance=profile)
        user_form=UserInfoForm(instance=req.user)



    context={
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile
    }


    return render(req,'customers/cprofile.html',context)