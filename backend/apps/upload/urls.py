from django.urls import path
from apps.upload.views import UploadFileApiView, UserFileList, FileTemplateList

urlpatterns = [
    path("upload_file", UploadFileApiView.as_view(), name="upload_file"),
    path("get_file_data/<int:id>", UserFileList.as_view({"get": "list"})),
    path("file_template_data", FileTemplateList.as_view({"get": "list"})),
]
