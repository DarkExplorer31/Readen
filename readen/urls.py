"""
URL configuration for readen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static

from authentication.views import SignupView, LoginView
from read.views import ReadCornerView, UploadBookView, DeleteBookView, UpdateTitleView

urlpatterns = [
    path("admin/", admin.site.urls),
    # authentication
    path("", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path(
        "logout/",
        LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    # read
    path("read_corner/", ReadCornerView.as_view(), name="read_corner"),
    path("upload_book/", UploadBookView.as_view(), name="upload_book"),
    path("update_title/", UpdateTitleView.as_view(), name="update_title"),
    path("delete_book/", DeleteBookView.as_view(), name="delete_book"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
