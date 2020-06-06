from django.urls import path
from . import views


app_name = 'dataset'


urlpatterns = [
    path("new/", views.CreateDataset.as_view(), name="create"),
    path("list/", views.UserDataset.as_view(), name="list"),
    path("delete/<int:pk>/", views.DeleteDataset.as_view(), name="delete"),
    path("detail/<int:pk>/", views.detail, name="detail"),
]