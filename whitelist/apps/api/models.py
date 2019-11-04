from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class UserKey(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.SET_NULL,related_name="usernames", null=True)
    key = models.CharField(_("Key"), max_length=100, db_index=True, null=True, blank=True)
    host = models.CharField(_("Host"), max_length=100, db_index=True, null=True, blank=True)

    class Meta:
        verbose_name = "UserKey"
        verbose_name_plural = "UserKey"
    
    def __unicode__(self):
        return str(self.key)



class AssignPort(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.SET_NULL,related_name="users", null=True)
    assigned_port = models.IntegerField(null=False, blank=False)
    user_ip = models.CharField(_("User_IP"), max_length=50, db_index=True, null=False, blank=False)
    user_port = models.IntegerField(null=False, blank=False)
    is_enable = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AssignPort"
        verbose_name_plural = "AssignPort"
    
    def __unicode__(self):
        return str(self.assigned_port)