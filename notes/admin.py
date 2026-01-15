from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Note, Tag


# Расширяем стандартную админку User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_note_count']

    def get_note_count(self, obj):
        return obj.note_set.count()

    get_note_count.short_description = 'Количество заметок'


# Регистрируем модели в админке
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at', 'get_tags']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['title', 'content', 'user__username']

    def get_tags(self, obj):
        return obj.get_tags_as_string()

    get_tags.short_description = 'Теги'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_note_count']
    search_fields = ['name']

    def get_note_count(self, obj):
        return obj.note_set.count()

    get_note_count.short_description = 'Количество заметок'