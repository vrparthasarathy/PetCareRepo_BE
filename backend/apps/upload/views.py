from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import DataFileSerializer
from .models import UploadFileDetails
import datetime
import os
import random
import pandas as pd
from openpyxl import load_workbook


def is_file_valid(file, file_extension):
    try:
        if file_extension == '.xlsx':
            load_workbook(file)
            return True
        elif file_extension == '.csv':
            pd.read_csv(file)
            return True
        else:
            return False
    except Exception:
        return False


class UploadFileApiView(APIView):
    """
    A simple ViewSet for uploading files.
    """
    def post(self, request):
        # Upload file & validate data
        import json
        reqData = json.loads(request.data['user'])
        user_id = reqData['id']

        serializer = DataFileSerializer(data=request.FILES)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        # user_id = UploadFileDetails.objects.last()

        uploaded_file = request.FILES['file_path']
        original_file_name = uploaded_file.name
        file_name = os.path.splitext(original_file_name)[0]
        file_extension = os.path.splitext(original_file_name)[1]  # Get the file extension
        unique_file_name = f"{user_id}_{file_name}_{random.randint(1000,9999)}{file_extension}"
        if not is_file_valid(uploaded_file, file_extension):
            return Response({'data': 'File format is not valid/corrupt'}, status=400)
        # data_file = UploadFileDetails.objects.create(file_path=uploaded_file, user_id=str(user_id.id+1))
        data_file = UploadFileDetails.objects.create(file_path=uploaded_file, user_id=str(user_id))
        data_file.file_path.save(unique_file_name, uploaded_file, save=True)
        data_file.upload_time = datetime.datetime.now()

        data_file.file_name = unique_file_name
        data_file.status = "success"
        data_file.save()
        return Response({'data': 'success'}, status=status.HTTP_200_OK)


class UserFileList(viewsets.ViewSet):
    """
    A simple ViewSet for listing user uploaded files.
    """
    def list(self, request, id=None):
        if id is None:
            return Response({"error": "Please provide the id"}, status=404)
        if data_file := UploadFileDetails.objects.filter(user_id=id):
            serializer = DataFileSerializer(data_file, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Data file not found"}, status=404)
