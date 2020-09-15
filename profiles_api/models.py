from django.db import models
from django.conf import settings #imports settings.py
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.
# Custom model manager
class UserProfileManager(BaseUserManager):
    """Manager for User profiles"""

    def create_user(self, email, name, password=None): # None will not work use hash
        """Create a new user profile"""  
        if not email:
            raise ValueError('User must provide an email address')
        # Email first part is case sensitive and second part is insensitive
        email = self.normalize_email(email)
        user = self.model(email=email, name=name) # Can't pass pwd for security

        user.set_password(password) # Encryption
        user.save(using=self._db) # Recommended although available by default

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

# Custom model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager() # Model manager custom 

    USERNAME_FIELD = 'email' # Replacing username field with email
    REQUIRED_FIELDS = ['name']


    def get_full_name(self):
        """Retrieve full name of the user""" 
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of the user""" 
        return self.name

    def __str__(self): # Recommended
        """Return string representation of the user"""
        return self.email

# Feed item

class ProfileFeedItem(models.Model):
    """Profile status update"""

    # PK FK rlnshp b/w user profile and feed
    # user_profile = models.ForeignKey(UserProfile)- do not hardcode
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """return the model as a string"""
        return self.status_text