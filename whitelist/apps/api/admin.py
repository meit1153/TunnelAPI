from django.contrib import admin
from .models import UserKey, AvailablePort, AssignPort

# Register your models here.

class UserKeyAdmin(admin.ModelAdmin):
  list_display = ('user', 'key')
  
class AvailablePortAdmin(admin.ModelAdmin):
  list_display = ('portno', 'is_available')

class AssignPortAdmin(admin.ModelAdmin):
  list_display = ('user', 'key', 'assigned_port', 'user_ip', 'user_port', 'is_enable')


admin.site.register(UserKey, UserKeyAdmin)
admin.site.register(AvailablePort, AvailablePortAdmin)
admin.site.register(AssignPort, AssignPortAdmin)