# from django.contrib import admin
# from .models import SigninUser
# from .models import contact

# # Register your models here.

# admin.site.register(SigninUser)
# admin.site.register(contact)



# admin.py
from django.contrib import admin
from .models import SigninUser
from .models import Contact  # Update the import
from .models import NutritionModel  # Update the import
from .models import MealInstructionModel


# Register your models here.
admin.site.register(SigninUser)
admin.site.register(Contact)  
admin.site.register(NutritionModel)  


class MealInstructionModelAdmin(admin.ModelAdmin):
    list_display = ('required_meal_age',)

admin.site.register(MealInstructionModel, MealInstructionModelAdmin)



