from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView as login

urlpatterns = [
    path('login', login.as_view()),
    path('cms_forms/', include('cms_forms.urls')),
    path('admin/', admin.site.urls),
]
