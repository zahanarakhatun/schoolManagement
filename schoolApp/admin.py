from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TeacherModel, Student

# Custom User Model Admin Panel-এ সুন্দরভাবে দেখানোর জন্য
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

# Admin Panel-এ Model গুলো Register করা
admin.site.register(User, CustomUserAdmin)
admin.site.register(TeacherModel)
admin.site.register(Student)