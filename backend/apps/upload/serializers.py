from rest_framework import serializers
from .models import UploadFileDetails


class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFileDetails
        fields = '__all__'
