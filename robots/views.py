from django.http import HttpResponse
from openpyxl import Workbook
from .models import Robot
from datetime import datetime, timedelta


def get_robot_production_data():
    today = datetime.today()
    last_week = today - timedelta(days=7)
    robots = Robot.objects.filter(created__gte=last_week)
    data = {}
    for robot in robots:
        model = robot.model
        version = robot.version
        if model not in data:
            data[model] = {}
        if version not in data[model]:
            data[model][version] = 0
        data[model][version] += 1
    return data


def excel_view(request):
    data = get_robot_production_data()
    wb = Workbook()
    ws = wb.active
    for model, versions in data.items():
        ws.append([model])
        for version, count in versions.items():
            ws.append([version, count])
        ws.append([])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=robot_production.xlsx'
    wb.save(response)
    return response
