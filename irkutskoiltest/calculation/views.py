import pandas as pd, numpy as np, openpyxl, calendar

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from datetime import datetime as dt

from .models import FallRate, Well, WaterCutCatalog
from .serializers import WellSerializer, FileUploadSerializer

# Create your views here.
def index(request):
    return render(request, 'index.html')

def add_months(start_date):
    current_date = start_date
    year = current_date.year
    if current_date.month == 12:
        year+= 1
    month = (current_date.month + 1) % 12 or 12
    day = min(current_date.day, calendar.monthrange(year, month)[1])
    new_date = current_date.replace(year=year, month=month, day=day)
    days_diff = (new_date - current_date).days
    return (days_diff, new_date)


class ExcelUploadAPIView(APIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = FileUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file,usecols=range(6))

            columns_old = df.columns.tolist()
            new_columns = ['title', 'liquid_yield', 'oil_yield', 'oil_produced', 'oil_reserve','water_cut']

            df = df.rename(columns={columns_old[i]: new_columns[i] for i in range(6)})
            duplicate_titles = df[df.duplicated('title', keep=False)]
            if not duplicate_titles.empty:
                return HttpResponseRedirect('/duplicate/')

            json_data = df.to_dict(orient='records')
            Well.objects.bulk_create([Well(**item) for item in json_data])
            table_serializer = WellSerializer(data=json_data, many=True)
            if table_serializer.is_valid():
                table_serializer.save()
                return HttpResponseRedirect('/success/')
            else:
                return Response(table_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExportToExcelView(APIView):
    def post(self, request):
        if request.method == 'POST':
            count_month = int(request.POST.get('count_month'))
            well_data = Well.objects.all()
            #fall_rate_data = FallRate.objects.all()
            water_cut_data = WaterCutCatalog.objects.all()
            oil_density = 0.829
            data_dict = {}
            for row in well_data:
                liquid_yield_actual = row.liquid_yield
                #liquid_yield_first = row.liquid_yield
                oil_yield_actual = row.oil_yield
                oil_produced_actual = row.oil_produced
                oil_reserve_actual = row.oil_reserve
                proportion_actual = oil_produced_actual/oil_reserve_actual
                water_cut_actual = 1 - (oil_yield_actual / (liquid_yield_actual * oil_density))
                title_actual = row.title
                data_dict[title_actual] = {}
                start_date=dt.today()
                for i in range(1, count_month + 1):
                    days_diff, new_date = add_months(start_date)
                    period = f'{dt.strftime(start_date,"%Y-%m-%d")} - {dt.strftime(new_date,"%Y-%m-%d")}'
                    data_dict[title_actual][period] = days_diff * oil_yield_actual
                    #data_dict[title_actual][period] = '; '.join([str(i) for i in [oil_produced_actual,oil_reserve_actual,water_cut_actual,days_diff,proportion_actual,days_diff * oil_yield_actual]])
                    oil_produced_actual += days_diff * oil_yield_actual
                    oil_reserve_actual -= days_diff * oil_yield_actual

                    #liquid_yield_actual = liquid_yield_first * fall_rate_data.filter(month=i+1).first().first_m * fall_rate_data.filter(month=i+1).first().second_m
                    oil_yield_actual = liquid_yield_actual * (1 - water_cut_actual) * oil_density
                    proportion_actual = oil_produced_actual / oil_reserve_actual
                    water_cut_actual = np.interp(proportion_actual, list(water_cut_data.values_list('water_cut_value', flat=True)), list(water_cut_data.values_list('first_characteristic', flat=True)))

                    start_date = new_date

            workbook = openpyxl.Workbook()

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="well_data.xlsx"'

            for sheet_name, sheet_data in data_dict.items():
                sheet = workbook.create_sheet(title=sheet_name)
                sheet.append(['period', 'oil_yield'])
                for key, value in sheet_data.items():
                    sheet.append([key, value])

            workbook.remove(workbook['Sheet'])
            workbook.save(response)

            return response





class SuccessUpload(View):
    def get(self, request):
        return render(request, 'success.html')

class Duplicate(View):
    def get(self, request):
        return render(request, 'duplicate.html')