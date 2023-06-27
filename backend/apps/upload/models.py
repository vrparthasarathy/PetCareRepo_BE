from django.db import models
# from django.utils import timezone

# Create your models here.


class FileType(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=True)
    path = models.FileField("file_path", upload_to='apps/upload/file', default=None)

    def __str__(self):
        return self.name.upper()

    class Meta:
        db_table = "filetype"


class User(models.Model):
    id = models.SmallIntegerField(primary_key=True, unique=True)
    EffemId = models.EmailField(max_length=254)

    def __str__(self):
        return self.EffemId

    class Meta:
        db_table = "user"


class FileStatus(models.Model):
    id = models.SmallIntegerField(primary_key=True, unique=True)
    status = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.status

    class Meta:
        db_table = "file_status"


class UploadFileDetails(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=True)
    filetypeid = models.ForeignKey(FileType, default=None, on_delete=models.CASCADE, db_column="filetypeid")
    status = models.ForeignKey(FileStatus, default=None, on_delete=models.CASCADE, db_column="StatusId")
    user_id = models.ForeignKey(User, default=None, on_delete=models.CASCADE, db_column="UploadedBy")
    UploadedOn = models.DateTimeField(auto_now_add=True)
    FilePath = models.FileField("file_path", upload_to='apps/upload/file', default=None)
    ErrorFilePath = models.FileField("error_file_path", upload_to='apps/upload/error', default=None)
    CreatedBy = models.SmallIntegerField(null=True)
    CreatedOn = models.DateTimeField(auto_now_add=True)
    LastUpdatedBy = models.SmallIntegerField(null=True)
    LastUpdatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.upper()

    class Meta:
        db_table = "uploadfiledetails"


class Rule(models.Model):
    id = models.SmallIntegerField(primary_key=True, unique=True)
    filetypeid = models.ForeignKey(FileType, default=None, on_delete=models.CASCADE, db_column="filetypeid")
    Rule = models.CharField(max_length=200, null=True)
    CreatedBy = models.SmallIntegerField(null=True)
    CreatedOn = models.DateTimeField(auto_now_add=True)
    LastUpdatedBy = models.SmallIntegerField(null=True)
    LastUpdatedOn = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rule"
