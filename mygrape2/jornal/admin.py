from django.contrib import admin

from .models import Location, Notes, GreenOper, Feeding, Processing

# Register your models here.
admin.site.register(Location)
admin.site.register(Notes)
admin.site.register(GreenOper)
admin.site.register(Feeding)
admin.site.register(Processing)

