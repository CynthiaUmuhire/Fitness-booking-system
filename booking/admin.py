from django.contrib import admin
from .models import UserProfile, FitnessClass, Booking

admin.site.register(UserProfile)
admin.site.register(FitnessClass)
admin.site.register(Booking)