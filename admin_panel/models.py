from django.db import models

from django.utils import timezone

class HomePageLayout(models.Model):
    title = models.CharField(max_length=300, default=None, blank=True, null=True)
    body_text = models.CharField(max_length=300, default=None, blank=True, null=True)
    image = models.ImageField(upload_to='images/posts/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.title)

