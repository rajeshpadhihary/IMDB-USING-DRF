from django.contrib import admin
from .models import Review,PlatformForStreaming,Movie

admin.site.register(Movie)
admin.site.register(PlatformForStreaming)
admin.site.register(Review)
