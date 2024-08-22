from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email).lower()  # Convert to lowercase
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # ... rest of the code remains the same

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)  # Add this field
    company_name = models.CharField(max_length=100)  # Add this field
    job_role = models.CharField(max_length=100)  # Add this field
    mycompany_id = models.CharField(max_length=10)  # Add this field
    tag_id = models.CharField(max_length=50)  # Add this field
    job_location = models.CharField(max_length=100)  # Add this field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    sites = models.ManyToManyField('Site', blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location']

    def __str__(self):
        return self.email
    
    
from django.core.validators import FileExtensionValidator

import os

def user_image_upload_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'facial_data/{instance.get_folder_name()}/{base_filename}{file_extension}'

class UserEnrolled(models.Model):
    sr = models.AutoField(primary_key=True, unique=True)
    picture = models.ImageField(upload_to='user_pictures/', blank=True, null=True)
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    mycompany_id = models.CharField(max_length=10)
    tag_id = models.CharField(max_length=50)
    job_location = models.CharField(max_length=100)
    orientation = models.FileField(upload_to='attachments/', blank=True, null=True, validators=[FileExtensionValidator(['jpeg', 'jpg'])])
    facial_data = models.ImageField(upload_to=user_image_upload_path, blank=True, null=True, verbose_name='Facial Data')
    my_comply = models.ImageField(upload_to='compliance_images/', blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    ], default='pending')
    email = models.EmailField()
    password = models.CharField(max_length=50)
    site = models.ForeignKey('Site', on_delete=models.CASCADE, blank=True, null=True)

    def _str_(self):
        return self.name

    def get_folder_name(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
        
from django.db.models.signals import post_delete
from django.dispatch import receiver
import shutil

@receiver(post_delete, sender=UserEnrolled)
def delete_user_folder(sender, instance, **kwargs):
    user_folder = os.path.join('media', 'facial_data', instance.get_folder_name())
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
    
class Notification(models.Model):
    sr = models.AutoField(primary_key=True,unique=True)
    subject = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.subject

class Upload_data(models.Model):
    #uploaded_file = models.FileField(upload_to='uploads/') # it takes all files 
    uploaded_file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpeg', 'jpg'])])
  
    def __str__(self):
        return str(self.uploaded_file)
    
class Site_management(models.Model):
    link_field = models.URLField(max_length=200) 

class Asset(models.Model):
    asset_id = models.IntegerField(unique=True)
    picture = models.ImageField(upload_to='asset_pictures/', blank=True, null=True)
    asset_name = models.CharField(max_length=255)
    tag_id = models.IntegerField()
    footage = models.ImageField(upload_to='assets_footage/', blank=True, null=True, verbose_name='Footage')
    description = models.CharField(max_length=500)
    asset_category = models.CharField(max_length=50)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    location = models.CharField(max_length=100, blank=True, null=True)
    time_log = models.DateTimeField(auto_now=True)
    site = models.ForeignKey('Site', on_delete=models.CASCADE)

    def _str_(self):
        return self.asset_name

    def check_file_exists(self, file_field):
        if file_field and os.path.isfile(os.path.join(settings.MEDIA_ROOT, file_field.name)):
            return True
        return False

    def check_picture_exists(self):
        return self.check_file_exists(self.picture)

    def check_footage_exists(self):
        return self.check_file_exists(self.footage)


class check_changes(models.Model):
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True) 
   
class Site(models.Model):
    picture = models.ImageField(upload_to='site_pictures/', blank=True, null=True)
    name = models.CharField(max_length=100,unique=True)
    location = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Site, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class company(models.Model):
    sr = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=100)
    works = models.CharField(max_length=100)
    safety_insurance = models.FileField(upload_to='attachments/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpeg', 'jpg'])])
    insurance_expiry = models.DateField()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            last_instance = self.__class__.objects.last()
            if last_instance:
                self.sr = last_instance.sr + 1
            else:
                self.sr = 1
        super().save(*args, **kwargs)

class timeschedule(models.Model):
    group = models.CharField(max_length=100)
    active_time = models.CharField(max_length=50)
    inactive_time = models.CharField(max_length=50)
    site = models.ForeignKey('Site', on_delete=models.CASCADE)

    def __str__(self):
        return self.group
    
class Upload_File(models.Model):
    #uploaded_file = models.FileField(upload_to='uploads/') # it takes all files 
    uploaded_file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpeg', 'jpg'])])

class Turnstile_S(models.Model):
    sr_no = models.AutoField(primary_key=True,unique=True)
    turnstile_id = models.IntegerField(unique=True)
    location = models.CharField(max_length=100)
    safety_confirmation = models.BooleanField(default=False)
    unlock = models.BooleanField(default=False)
    site = models.ForeignKey('Site', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.turnstile_id)
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            last_instance = self.__class__.objects.last()
            if last_instance:
                self.sr_no = last_instance.sr_no + 1
            else:
                self.sr_no = 1
        super().save(*args, **kwargs)

class Orientation(models.Model):
    attachments = models.FileField(upload_to='attachments/', validators=[FileExtensionValidator(['pdf'])])

class PreShift(models.Model):
    document = models.FileField(upload_to='preshift/') 
    date = models.DateField(auto_now_add=True) 
    site = models.ForeignKey('Site', on_delete=models.CASCADE)

class ToolBox(models.Model):
    document = models.FileField(upload_to='toolbox/') 
    date = models.DateField(auto_now_add=True) 
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    
class OnSiteUser(models.Model):
    name = models.CharField(max_length=100)
    tag_id = models.CharField(max_length=50)
    status = models.CharField(max_length=100, choices=[
        ('Entry', 'Entry'),
        ('Exit', 'Exit'),
    ])
    timestamp = models.DateTimeField(auto_now=True) 
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    face = models.BooleanField(default=False)  # Field to store 1 (True) or 0 (False)
    
    def __str__(self):
        return self.name
    
    


class UpdateStatus(models.Model):
    last_update = models.DateTimeField(default=timezone.now)
    dataset_updated = models.BooleanField(default=False)

    @classmethod
    def get_or_create_status(cls):
        status, created = cls.objects.get_or_create(pk=1)
        return status
    
    
    
from django.db import models
import os
from django.conf import settings

class FolderState(models.Model):
    folder_name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    modification_time = models.DateTimeField()

    class Meta:
        unique_together = ('folder_name', 'file_name')

    def __str__(self):
        return f"{self.folder_name}/{self.file_name}"
