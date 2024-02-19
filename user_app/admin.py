from django.contrib import admin
from .models import Users

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('Email_Address', 'name','zipcode','is_active','is_admin','is_online','is_superuser')
    search_fields = ['name']