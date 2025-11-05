from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RideUser, Ride, RideEvent

@admin.register(RideUser)
class RideUserAdmin(UserAdmin):
    search_fields = ('username', 'email',)

    list_filter = ('role', 'is_active',)
    
    list_display = (
        'id',
        'username', 
        'email',
        'first_name', 
        'last_name', 
        'role', 
        'is_active',
    )
    
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Authentication', {'fields': ('username', 'email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('role', 'is_active',)}),
    )


class RideEventInline(admin.StackedInline):
    model = RideEvent
    readonly_fields = ('description', 'created')


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    search_fields = ('driver__username', 'rider__username')
    
    list_display = ('id', 'rider', 'driver', 'status', 'pickup_time',)
    
    list_filter = ('status', 'pickup_time',)
    
    ordering = ('-pickup_time',)

    inlines = [RideEventInline]


@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    search_fields = ('ride__id', 'description')
    
    list_display = ('id', 'ride', 'description', 'created',)
    
    list_filter = ('created',)
    
    ordering = ('-created',)
