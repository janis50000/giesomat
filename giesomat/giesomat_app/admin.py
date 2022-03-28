from django.contrib import admin
from .models import PlantTechnical, Plant, Sensor, Pump, Valve

#class ChoiceInline(admin.StackedInline):

class PlantTechnicalInline(admin.TabularInline):
    model = PlantTechnical
    extra = 1

class PlantAdmin(admin.ModelAdmin):
    inlines = [PlantTechnicalInline]
    exclude = ['current_status']
    list_display = ('plant_name', 'water_need', 'is_active', 'current_status', 'water_mode')
    list_filter = ['is_active', 'current_status', 'water_mode']
    search_fields = ['plant_name']

admin.site.register(Plant, PlantAdmin)
admin.site.register(PlantTechnical)
admin.site.register(Sensor)
admin.site.register(Pump)
admin.site.register(Valve)

