from django.contrib import admin
from .models import Language, Level, Teacher, Course, CourseMaterial, Enrollment
from django.utils import timezone

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    filter_horizontal = ['languages']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'level', 'price', 'teacher', 'is_active']
    list_filter = ['language', 'level', 'is_active']

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'uploaded_at']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'application_date', 'status', 'processed_date']
    list_filter = ['status', 'application_date']
    actions = ['approve_selected', 'reject_selected']

    def approve_selected(self, request, queryset):
        queryset.update(status='approved', processed_date=timezone.now())
        self.message_user(request, "Выбранные заявки подтверждены")

    def reject_selected(self, request, queryset):
        queryset.update(status='rejected', processed_date=timezone.now())
        self.message_user(request, "Выбранные заявки отклонены")

    approve_selected.short_description = "Подтвердить выбранные заявки"
    reject_selected.short_description = "Отклонить выбранные заявки"

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)