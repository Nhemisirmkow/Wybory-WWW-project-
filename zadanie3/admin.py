from django.contrib import admin
from zadanie2.models import Kandydat, Kandydat_Województwo, Kandydat_Okręg, Kandydat_Gmina, Gmina, Okręg, Województwo, \
    Test


# Register your models here.

class TestAdmin(admin.ModelAdmin):
    search_fields = []

class KandydatAdmin(admin.ModelAdmin):
    search_fields = []

class KandydatWojewództwoAdmin(admin.ModelAdmin):
    search_fields = ['nazwa', 'województwo']

class KandydatOkręgAdmin(admin.ModelAdmin):
    search_fields = ['nazwa', 'okręg']

class KandydatGminaAdmin(admin.ModelAdmin):
    search_fields = ['nazwa', 'gmina']

class GminaAdmin(admin.ModelAdmin):
    search_fields = ['nazwa']

class OkręgAdmin(admin.ModelAdmin):
    search_fields = ['nazwa']

class WojewództwoAdmin(admin.ModelAdmin):
    search_fields = ['nazwa']

admin.site.register(Test, TestAdmin)
admin.site.register(Kandydat, KandydatAdmin)
admin.site.register(Kandydat_Województwo, KandydatWojewództwoAdmin)
admin.site.register(Kandydat_Okręg, KandydatOkręgAdmin)
admin.site.register(Kandydat_Gmina, KandydatGminaAdmin)
admin.site.register(Gmina, GminaAdmin)
admin.site.register(Okręg, OkręgAdmin)
admin.site.register(Województwo, WojewództwoAdmin)