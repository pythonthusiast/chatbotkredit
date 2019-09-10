from django.contrib import admin
from .models import PengajuanKredit

class PengajuanKreditAdmin(admin.ModelAdmin):
    list_display = ('username', 'approve')


admin.site.register(PengajuanKredit, PengajuanKreditAdmin)
