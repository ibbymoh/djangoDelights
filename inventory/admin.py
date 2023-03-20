from django.contrib import admin
from .models import *
# Register your models here.


#
class IngredientAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",) }

class MenuItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",) }
class RecipeRequirementAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("ingredient",)}

admin.site.register(Ingredient,IngredientAdmin)
admin.site.register(RecipeRequirement,RecipeRequirementAdmin)
admin.site.register(MenuItem,MenuItemAdmin)
admin.site.register(Purchase)




