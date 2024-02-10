from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.conf import settings
import win32com.client
import pythoncom
import os

from .models import Contractor, ExcelFile


@csrf_exempt
def create_new_excel(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        data.pop(0)
        filtered_data = {}
        for i in range(0, len(data)):
            for j in range(0, 10):
                if data[i][j] != "":
                    filtered_data[data[i][j]] = [i, j]

        rand_int = random.randint(1, 10000)
        file_name = f"{request.user}_{rand_int}"
        file_path = str(settings.BASE_DIR / f"media/{file_name}")

        excel = win32com.client.gencache.EnsureDispatch("Excel.Application", pythoncom.CoInitialize())
        workbook = excel.Workbooks.Add()
        xl = workbook.Worksheets.Add()

        for value, indices in filtered_data.items():
            xl.Cells(indices[0] + 1, indices[1] + 1).Value = value

        workbook.SaveAs(file_path)
        workbook.Close()
        excel.Quit()

        contractor = Contractor.objects.get(user=request.user)
        ExcelFile.objects.create(contractor=contractor, file=f'{file_name}.xlsx')
    
    else:
        return render(request, "index.html")


from django.http import HttpResponse
from .models import ExcelFile


def download_excel(request, id):
    try:
        excel_file = ExcelFile.objects.get(id=id)
        
        with open(excel_file.file.path, "rb") as file:
            response = HttpResponse(file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = f'attachment; filename="{os.path.basename(excel_file.file.name)}"'
            return response
    except ExcelFile.DoesNotExist:
        return HttpResponse("Excel file not found", status=404)
