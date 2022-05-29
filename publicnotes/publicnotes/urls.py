from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wall.urls'))
]

handler404 = 'wall.views.handle_page_not_found'
