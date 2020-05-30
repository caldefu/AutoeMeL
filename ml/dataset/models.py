from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class DatasetModel (models.Model):
    user = models.ForeignKey(User, related_name='datasets', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    

    def __str__ (self):
        return self.name
