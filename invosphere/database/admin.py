from django.contrib import admin
from database.models import Billing

class xyz(admin.ModelAdmin):
    pass
admin.site.register(Billing,xyz)
