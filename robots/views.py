
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Robot
import json


@require_http_methods(["POST"])
def create_robot(request):
    try:
        data = json.loads(request.body)
        model = data.get('model')
        version = data.get('version')
        created = data.get('created')

        if not Robot.objects.filter(model=model).exists():
            return JsonResponse({'error': 'Модель робота не существует'}, status=400)

        robot = Robot(model=model, version=version, created=created)
        robot.save()
        return JsonResponse({'message': 'Робот создан успешно'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
