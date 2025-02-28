from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        # Create a UserProfile when a new user is created
        UserProfile.objects.create(user=instance)
    else:
        try:
            # Check if the profile exists
            profile = UserProfile.objects.get(user=instance)

            # You can add profile updates here if needed
            profile.save()  
        except UserProfile.DoesNotExist:
            # If no profile exists, create one
            UserProfile.objects.create(user=instance)


# post_save.connect(post_save_create_profile,sender=User)
