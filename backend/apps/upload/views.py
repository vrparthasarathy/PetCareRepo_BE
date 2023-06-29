from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import DataFileSerializer, FileTemplateSerializer
from .models import UploadFileDetails, FileStatus, User, FileTemplate, FileTemplateField
import datetime
import os
import pandas as pd
from openpyxl import load_workbook
import json


class UploadFileApiView(APIView):
    """
    A simple ViewSet for uploading files.
    """
    def post(self, request):
        # Upload file & validate data

        reqData = json.loads(request.data["user"])
        user_id = reqData["id"]
        tempid = request.data["tempid"]
        serializer = DataFileSerializer(data=request.FILES)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        # user_id = UploadFileDetails.objects.last()

        uploaded_file = request.FILES["file"]
        original_file_name = uploaded_file.name
        file_name = os.path.splitext(original_file_name)[0]
        file_extension = os.path.splitext(original_file_name)[
            1
        ]  # Get the file extension
        unique_file_name = f"{file_name}_{user_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
        if not self.is_file_valid(tempid, uploaded_file, file_extension):
            response_data = {
                'result': 'error',
                'message': 'file format is not valid',
            }
            return Response(response_data, status=400)
        # data_file = UploadFileDetails.objects.create(file_path=uploaded_file, user_id=str(user_id.id+1))
        file_path = os.path.join('apps/upload/file/', unique_file_name)
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        try:
            return self.extracted_data_from_table(user_id, tempid, unique_file_name)
        except Exception as e:
            response_data = {
                'result': 'error',
                'message': f"Internal server error occurred/ {e}"
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def is_file_valid(self, id, file, file_extension):
        try:
            if file_extension in [".xlsx", ".xls"]:
                load_workbook(file)
                df = pd.read_excel(file)

            elif file_extension == ".csv":
                df = pd.read_csv(file)

            else:
                return False

            expected_columns = FileTemplateField.objects.filter(tempid=id).values('fieldname')
            columns = df.columns.tolist()
            return all(items['fieldname'] in set(columns) for items in expected_columns)

        except Exception:
            return False

    def extracted_data_from_table(self, user_id, tempid, unique_file_name):
        user_instance = User.objects.get(id=user_id)
        file_instance = FileTemplate.objects.get(id=tempid)
        file_status_instance = FileStatus.objects.get(pk=1)
        data_file = UploadFileDetails(
            user_id=user_instance,
            filetempid=file_instance,
            status=file_status_instance,
        )
        # data_file.FilePath.save(unique_file_name, uploaded_file, save=True)
        data_file.CreatedOn = datetime.datetime.now()
        data_file.name = unique_file_name

        data_file.save()
        response_data = {
                'result': 'Success',
                'message': 'Data Exists',
            }
        return Response(response_data, status=status.HTTP_200_OK)


class UserFileList(viewsets.ViewSet):
    """
    A simple ViewSet for listing user uploaded files.
    """
    def list(self, request, id=None):
        if id is None:
            response_data = {
                'result': 'error',
                'message': 'Please provide the id',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        if data_file := UploadFileDetails.objects.filter(user_id=id):
            serializer = DataFileSerializer(data_file, many=True)
            response_data = {
                'result': 'Success',
                'message': 'Data Exists',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'result': 'error',
                'message': 'Data not found',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class FileTemplateList(viewsets.ViewSet):
    """
    A simple ViewSet for listing File Template data.
    """
    def list(self, request):
        if data_list := FileTemplate.objects.all():
            serializer = FileTemplateSerializer(data_list, many=True)
            response_data = {
                'result': 'Success',
                'message': 'Data Exists',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'result': 'error',
                'message': 'Data not found',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
