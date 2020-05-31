from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ml.core import views
from ml.dataset import views as datasetviews



urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('secret/', views.secret, name='secret'),
    path('secret2/', views.SecretPage.as_view(), name="secret2"),
    path('dataset/', include('ml.dataset.urls', namespace='datasets')),   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)