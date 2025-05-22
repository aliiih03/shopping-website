from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    fields = ['first_name', 'last_name', 'username', 'email']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
