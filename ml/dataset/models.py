from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class Dataset (models.Model):
    user = models.ForeignKey(User, related_name='datasets', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, default='')
    

    def __str__ (self):
        return self.name
class Meta:
    unique_together = ['user', 'name']
    order = '-create_at'