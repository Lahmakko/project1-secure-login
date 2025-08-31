from django.contrib import admin
from django.urls import path, include  # include needed to pull app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # include app URLs
]
