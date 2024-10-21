from django.contrib import admin
from .models import AdvertisementRequest

@admin.register(AdvertisementRequest)
class AdvertisementRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad_content', 'created_at', 'is_completed')
    list_filter = ('is_completed', 'created_at')
    search_fields = ('user__login', 'ad_content')
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        queryset.update(is_completed=True)
        self.message_user(request, "Заявки отмечены как выполненные.")
    mark_as_completed.short_description = 'Отметить как выполненные'
