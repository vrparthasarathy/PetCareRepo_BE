from rest_framework import serializers
from .models import UploadFileDetails, FileTemplate


class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFileDetails
        fields = '__all__'


class FileTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTemplate
        fields = '__all__'
