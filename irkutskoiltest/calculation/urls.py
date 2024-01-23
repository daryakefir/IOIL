
from django.urls import path
from . import views
from .views import ExportToExcelView, ExcelUploadAPIView, SuccessUpload, Duplicate

urlpatterns = [
    path('export-to-excel/', ExportToExcelView.as_view(), name='export-to-excel'),
    path('success/', SuccessUpload.as_view(), name='success'),
    path('duplicate/', Duplicate.as_view(), name='duplicate'),
    path('excel-upload/', ExcelUploadAPIView.as_view(), name='excel-upload'),
    path('', views.index), #http://127.0.0.1:8000/
]
