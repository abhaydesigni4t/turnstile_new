import os
from django.utils import timezone
from .models import UserEnrolled, FolderState
from django.conf import settings


import logging

logger = logging.getLogger(__name__)

def update_folder_states():
    changed = False
    logger.info("Starting folder state update")
    
    for user in UserEnrolled.objects.all():
        folder_path = os.path.join(settings.MEDIA_ROOT, 'facial_data', user.get_folder_name())
        
        if not os.path.exists(folder_path):
            continue
        
        current_files = {}
        for filename in os.listdir(folder_path):
            if filename.endswith('.jpg') or filename.endswith('.jpeg'):
                file_path = os.path.join(folder_path, filename)
                mod_time = timezone.make_aware(timezone.datetime.fromtimestamp(os.path.getmtime(file_path)))
                current_files[filename] = mod_time
        
        db_files = FolderState.objects.filter(folder_name=user.get_folder_name())
        db_files_map = {f"{file.file_name}": file.modification_time for file in db_files}
        
        logger.info(f"Current files: {current_files}")
        logger.info(f"DB files: {db_files_map}")

        for filename, mod_time in current_files.items():
            if filename not in db_files_map or db_files_map[filename] != mod_time:
                FolderState.objects.update_or_create(
                    folder_name=user.get_folder_name(),
                    file_name=filename,
                    defaults={'modification_time': mod_time}
                )
                logger.info(f"File changed or added: {filename}")
                changed = True
        
        files_to_remove = set(db_files_map.keys()) - set(current_files.keys())
        if files_to_remove:
            FolderState.objects.filter(
                folder_name=user.get_folder_name(),
                file_name__in=files_to_remove
            ).delete()
            logger.info(f"Files removed: {files_to_remove}")
            changed = True

    return changed
