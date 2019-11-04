from django.contrib import admin
from .models import UserKey, AssignPort

# Register your models here.

class UserKeyAdmin(admin.ModelAdmin):
  list_display = ('user', 'key', 'host')
  

class AssignPortAdmin(admin.ModelAdmin):
  list_display = ('user', 'assigned_port', 'user_ip', 'user_port', 'is_enable')


admin.site.register(UserKey, UserKeyAdmin)
admin.site.register(AssignPort, AssignPortAdmin)