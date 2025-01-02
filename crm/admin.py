from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SuperAdmin)
admin.site.register(Company)
admin.site.register(User)
admin.site.register(Template)
admin.site.register(WhatsApp_Group)
admin.site.register(Group_Contacts)
admin.site.register(MessageLog)
