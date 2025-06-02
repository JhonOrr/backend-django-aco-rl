# vrp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .services.aco_vrp import ACOVRPPD_MultiVehicle  # Importar tu clase

@csrf_exempt
def run_aco(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extraer parámetros del frontend
            num_ants = data.get('num_ants', 20)
            iterations = data.get('iterations', 200)
            evaporation_rate = data.get('evaporation_rate', 0.1)
            alpha = data.get('alpha', 1)
            beta = data.get('beta', 3)
            vehicles = data.get('vehicles')
            nodes = data.get('nodes')

            if not vehicles or not nodes:
                return JsonResponse({'error': 'Faltan vehículos o nodos.'}, status=400)
            
            # Ejecutar el algoritmo
            aco = ACOVRPPD_MultiVehicle(
                num_ants=num_ants,
                iterations=iterations,
                evaporation_rate=evaporation_rate,
                alpha=alpha,
                beta=beta,
                vehicles=vehicles,
                nodes=nodes
            )

            best_routes, best_distance = aco.run()

            # Preparar respuesta
            result = {
                'best_routes': best_routes,
                'best_distance': best_distance
            }
            return JsonResponse(result, safe=False)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
