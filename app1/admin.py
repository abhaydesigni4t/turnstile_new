from django.contrib import admin
from .models import UserEnrolled,CustomUser,Notification,Upload_data,Asset,check_changes,Site,company,timeschedule,Upload_File,Turnstile_S,Orientation,PreShift,ToolBox,OnSiteUser

admin.site.register(CustomUser)
admin.site.register(UserEnrolled)
admin.site.register(Notification)
admin.site.register(Upload_data)
admin.site.register(Asset)
admin.site.register(check_changes)
admin.site.register(Site)
admin.site.register(company)
admin.site.register(timeschedule)
admin.site.register(Upload_File)
admin.site.register(Turnstile_S)
admin.site.register(Orientation)
admin.site.register(PreShift)
admin.site.register(ToolBox)
admin.site.register(OnSiteUser)
