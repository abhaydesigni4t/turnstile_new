from django.db.models.signals import post_save, pre_delete,post_delete
from django.dispatch import receiver
from django.core.cache import cache
from datetime import datetime
import os
from .models import UserEnrolled,Asset

@receiver(post_save, sender=UserEnrolled)
def book_change_handler(sender, instance, **kwargs):
    cache.set('has_changes', True)

@receiver(pre_delete, sender=UserEnrolled)
def book_delete_handler(sender, instance, **kwargs):
    cache.set('has_changes', True)



@receiver(post_save, sender=UserEnrolled)
def create_user_folder(sender, instance, created, **kwargs):
    if created:
        user_folder = os.path.join('media', 'facial_data', instance.get_folder_name())
        os.makedirs(user_folder, exist_ok=True)

        # Get all images in the user's facial_data folder
        user_images = [f for f in os.listdir(user_folder) if f.endswith('.jpg') or f.endswith('.jpeg')]

        if user_images:
            # Check if the current picture is deleted or not in the user's folder
            if instance.picture and os.path.basename(instance.picture.name) not in user_images:
                # Find the next available image and set it as the user's picture
                for image in user_images:
                    if image != os.path.basename(instance.picture.name):
                        instance.picture = os.path.join('facial_data', instance.get_folder_name(), image)
                        instance.save()
                        break
            elif not instance.picture:
                # If there's no current picture, set the first image as the user's picture
                first_image = user_images[0]
                instance.picture = os.path.join('facial_data', instance.get_folder_name(), first_image)
                instance.save()
        else:
            instance.picture = None  # No image found, set picture to None or another default value
            instance.save()
            

from .models import UpdateStatus
from django.utils import timezone
   
@receiver(post_save, sender=UserEnrolled)
def update_status_on_save(sender, instance, **kwargs):
    status = UpdateStatus.get_or_create_status()
    status.last_update = timezone.now()
    status.dataset_updated = True
    status.save()

@receiver(post_delete, sender=UserEnrolled)
def update_status_on_delete(sender, instance, **kwargs):
    status = UpdateStatus.get_or_create_status()
    status.last_update = timezone.now()
    status.dataset_updated = True
    status.save()