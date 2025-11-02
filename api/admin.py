from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RideUser

@admin.register(RideUser)
class RideUserAdmin(UserAdmin):
    model = RideUser

    search_fields = ('username', 'email')

    list_filter = ('role', 'is_active')
    
    list_display = ('id','username', 'first_name', 'last_name', 'role', 'is_active')
    
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Authentication', {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('role', 'is_active',)}),
    )


