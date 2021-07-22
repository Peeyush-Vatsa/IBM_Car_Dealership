from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelInline class
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    pass
# CarMakeAdmin class with CarModelInline

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)