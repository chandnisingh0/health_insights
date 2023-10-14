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

# Register your models here.
admin.site.register(SigninUser)
admin.site.register(Contact)  # Update the registration for the Contact model