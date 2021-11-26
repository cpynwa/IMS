from django.contrib import admin
from django.contrib.admin.models import LogEntry
from import_export.admin import ImportExportModelAdmin
from .models import Data, Vendor, Location, Part, Status, Delivery


# Register your models here.
@admin.register(Data)
class DataAdmin(ImportExportModelAdmin):
    list_display = ["id", "serial", "get_part", "hostname", "get_status", "get_vendor", "get_location", "place"]
    list_display_links = ["id", "serial"]
    list_filter = ["part", "vendor", "location"]
    search_fields = ["serial", "hostname", "ipaddress"]

    def get_part(self, obj):
        return obj.part.part
    get_part.short_description = 'Parts'

    def get_vendor(self, obj):
        return obj.vendor.vendor
    get_vendor.short_description = 'vendor'

    def get_location(self, obj):
        return obj.location.location
    get_location.short_description = 'location'

    def get_status(self, obj):
        return obj.status.status
    get_status.short_description = 'status'

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["id", "vendor"]
    list_display_links = ["id", "vendor"]
    search_fields = ["vendor"]

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["id", "location", "address"]
    list_display_links = ["id", "location"]
    search_fields = ["location"]

@admin.register(Part)
class PartsAdmin(admin.ModelAdmin):
    list_display = ["id", "part", "part_number", "get_vendor"]
    list_display_links = ["id", "part"]
    search_fields = ["part", "part_number"]

    def get_vendor(self, obj):
        return obj.vendor.vendor
    get_vendor.short_description = 'vendor'

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "status"]
    list_display_links = ["id", "status"]

@admin.register(Delivery)
class DeliveryDataAdmin(admin.ModelAdmin):
    list_display = ["id", "creator", "created_date", "rma_num", "serial", "vendor", "part", "status"]
    list_display_links = ["id", "rma_num"]
    search_fields = ["id", "creator", "created_date", "rma_num", "serial", "vendor", "part", "status"]

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_string', 'action_time', 'object_id')
    actions = None

    def get_string(self, obj):
        return str(obj)

    get_string.short_description = 'action'

    def get_user(self, obj):
        return str(obj.user.username)
    get_user.short_description = 'User'

    search_fields = ['=user__username', ]
    fieldsets = [
        (None, {'fields':()}),
        ]

    def __init__(self, *args, **kwargs):
        super(LogEntryAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = None

admin.site.register(admin.models.LogEntry, LogEntryAdmin)