from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from my_app.media import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('Registration/', views.register, name="register"),
    path('sign_in/', views.sign_in, name="sign_in"),
    path('posting/', views.post, name="posting"),
    path('logout/', views.log_out, name="log_out"),
    path('post/<id>', views.show_post, name="show_post"),
    path('add_cm/<id>', views.add_cm, name="add_cm"),
    path('own_page', views.own_page, name="own_page"),
    path('add_like/<id>', views.add_like, name="add_like"),
    path('search', views.search, name="search"),
]
#we add our media pattern to url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
