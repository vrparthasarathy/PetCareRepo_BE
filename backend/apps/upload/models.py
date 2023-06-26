from django.db import models
# from django.utils import timezone

# Create your models here.


class UploadFileDetails(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_id = models.CharField(max_length=100, null=True)
    file_name = models.CharField(max_length=200, null=True)
    file_path = models.FileField(upload_to='apps/upload/')
    upload_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True)
    error = models.CharField(max_length=200, null=True)
    stored_time = models.DateTimeField(auto_now=True)
    last_updated_time = models.DateTimeField(auto_now=True)
