from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

# Custom manager for the User model
class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, password=None):
        """
        Method to create a regular user with necessary fields: first_name, last_name, username, email, and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')

        # Create the user object with the provided details
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        # Set the password and save the user
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        """
        Method to create a superuser (administrator) with extra permissions.
        """
        # Use the create_user method to create the user
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        
        # Set additional fields for a superuser
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# Custom User model extending AbstractBaseUser
class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    # Choices for user roles
    ROLE_CHOICE = (
        (VENDOR, "Vendor"),
        (CUSTOMER, "Customer")
    )

    # Fields for user model
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)
    
    # Date fields for tracking creation and modification times
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Fields for permission management
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # Set the email as the username field
    USERNAME_FIELD = 'email'
    # Required fields for user creation (besides password)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Assign the custom manager to the User model
    objects = UserManager()

    def __str__(self):
        """
        Return the string representation of the user (email).
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Check if the user has the given permission (e.g., admin rights).
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Check if the user has permissions for a given app module.
        """
        return True 
    def get_role(self):
        if self.role==1:
            user_role="Vendor"
        elif self.role==2:
            user_role="User"
        return user_role
    

# UserProfile model to store additional information about the user
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to User model
    profile_picture = models.ImageField(upload_to='users/profile_pictures', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    location=gismodels.PointField(blank=True,null=True,srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        """
        Return the string representation of the user profile (linked to the user's email).
        """
        return self.user.email

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.location = Point(float(self.longitude), float(self.latitude))

        super().save(*args, **kwargs)  