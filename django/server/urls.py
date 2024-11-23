
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(('core.urls', 'core'), namespace='core')),
    path('manage/', include(('field_mgmt.urls', 'field_mgmt'), namespace='field_mgmt')),
]
