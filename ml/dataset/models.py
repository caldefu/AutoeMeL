from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class Dataset (models.Model):
    user = models.ForeignKey(User, related_name='datasets', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, default='')
    archivo = models.FileField(upload_to='datasets/', null=False)
    

    def __str__ (self):
        return self.name

    def deslete(self, *args, **kwargs):
        self:archivo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        unique_together = ['user', 'name']
        ordering = ['-created_at']