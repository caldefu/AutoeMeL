from django.urls import path
from . import views


app_name = 'dataset'


urlpatterns = [
    path("new/", views.CreateDataset.as_view(), name="create"),
    path("list/", views.UserDataSets.as_view(), name="list"),
    
]