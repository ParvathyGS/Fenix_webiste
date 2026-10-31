from django.contrib import admin

from .models import ConsructionSite, SiteImage


class SiteImageInline(admin.TabularInline):
    model = SiteImage
    extra = 1


@admin.register(ConsructionSite)
class ConsructionSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_date', 'end_date', 'engineer_incharge')
    search_fields = ('name', 'location', 'engineer_incharge')
    inlines = [SiteImageInline]


@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ('site', 'caption', 'uploaded_at')
