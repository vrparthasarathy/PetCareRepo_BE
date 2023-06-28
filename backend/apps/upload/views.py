from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import DataFileSerializer
from .models import UploadFileDetails, FileStatus, User, FileTemplate, FileTemplateField
import datetime
import os
import pandas as pd
from openpyxl import load_workbook


def is_file_valid(id, file, file_extension):
    try:
        if file_extension in [".xlsx", ".xls"]:
            load_workbook(file)
            df = pd.read_excel(file)

        elif file_extension == ".csv":
            df = pd.read_csv(file)

        else:
            return False
        expected_columns = FileTemplateField.objects.filter(tempid=id).values('fieldname')

        # Check column names
        columns = df.columns.tolist()
        return all(items['fieldname'] in set(columns) for items in expected_columns)

    except Exception:
        return False


class UploadFileApiView(APIView):
    """
    A simple ViewSet for uploading files.
    """

    def post(self, request):
        # Upload file & validate data
        import json

        reqData = json.loads(request.data["user"])
        user_id = reqData["id"]
        tempid = request.data["tempid"]
        print(tempid)
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
        if not is_file_valid(tempid, uploaded_file, file_extension):
            return Response({"data": "File format is not valid/corrupt"}, status=400)
        # data_file = UploadFileDetails.objects.create(file_path=uploaded_file, user_id=str(user_id.id+1))
        file_path = os.path.join('apps/upload/file/', unique_file_name)
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

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
        return Response({"data": "Success"}, status=status.HTTP_200_OK)


class UserFileList(viewsets.ViewSet):
    """
    A simple ViewSet for listing user uploaded files.
    """

    def list(self, request, id=None):
        if id is None:
            return Response({"error": "Please provide the id"}, status=404)
        if data_file := UploadFileDetails.objects.filter(status=id):
            serializer = DataFileSerializer(data_file, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Data file not found"}, status=404)
