from django.contrib import admin

from .models import RainInAu

#Make the rainAU app modifiable in the admin
admin.site.register(RainInAu)
