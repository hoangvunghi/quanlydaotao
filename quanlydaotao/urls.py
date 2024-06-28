from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.urls')),
    path('api/', include('ketquahoctap.urls')),
    path('api/', include('dangkyhoc.urls')),
]
