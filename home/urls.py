from django.contrib.auth  import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)