# jobportal/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin site customizations
admin.site.site_header = "Developer Mandy"
admin.site.site_title = "Welcome to Mandy's Dashboard"
admin.site.index_title = "Welcome to this portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('job.urls')),  # Ensure this points to the correct app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
