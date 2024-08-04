from django.contrib import admin
from .models import AsmePipe
from .models import FlangeRating


# Register your models here.
admin.site.register(FlangeRating)

@admin.register(AsmePipe)
class AsmePipeAdmin(admin.ModelAdmin):
    list_display = ('dn', 'nps', 'sch', 'od', 'wt', 'mass')
    list_filter = ('dn', 'nps', 'sch',)
    ordering = ('dn', 'nps', 'sch', 'od',)
    search_fields = ('dn', 'nps', 'sch',)
