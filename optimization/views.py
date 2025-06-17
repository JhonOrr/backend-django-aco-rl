# vrp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import decimal
from orders.models import Order
from .services.aco_vrp import ACOVRPPD_MultiVehicle

@csrf_exempt
def run_aco(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 1. Extraer parámetros del frontend
            num_ants = data.get('num_ants', 20)
            iterations = data.get('iterations', 200)
            evaporation_rate = data.get('evaporation_rate', 0.1)
            alpha = data.get('alpha', 1)
            beta = data.get('beta', 3)
            vehicles = data.get('vehicles')
            
            if not vehicles:
                return JsonResponse({'error': 'Faltan vehículos.'}, status=400)
            
            # 2. Obtener órdenes de la base de datos
            orders = Order.objects.filter(status='Pendiente')
            
            if not orders.exists():
                return JsonResponse({'error': 'No hay órdenes pendientes para procesar'}, status=400)
                
            # 3. Construir lista de nodos a partir de las ordenes
            nodes = []
            
            # Agregar depósito (nodo 0)
            depot_lat = -12.087000
            depot_lng = -76.97180
            nodes.append(['depot', depot_lat, depot_lng, 0])
            
            # Contador para seguimiento de pares pickup-delivery
            node_counter = 1
            
            # Agregar nodos de órdenes (pickup y delivery)
            for order in orders:
                # Convertir Decimal a float para compatibilidad
                pickup_lat = float(order.pickup_lat)
                pickup_lng = float(order.pickup_lng)
                delivery_lat = float(order.delivery_lat)
                delivery_lng = float(order.delivery_lng)
                capacity = float(order.capacity)
                
                # Nodo PICKUP (demanda positiva)
                nodes.append(['pickup', pickup_lat, pickup_lng, capacity])
                
                # Nodo DELIVERY (demanda negativa)
                nodes.append(['delivery', delivery_lat, delivery_lng, -capacity])
                
                # Incrementar contador
                node_counter += 2
            
            # 4. Ejecutar el algoritmo
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

            # 5. Preparar respuesta estructurada
            result = {
                'best_distance': best_distance,
                'routes': []
            }
            
            # Construir respuesta detallada
            for route_idx, route in enumerate(best_routes):
                route_info = {
                    'vehicle_id': route_idx,
                    'capacity': vehicles[route_idx][0],
                    'max_distance': vehicles[route_idx][1],
                    'total_distance': 0,
                    'stops': []
                }
                
                # Calcular distancia total para esta ruta
                for i in range(len(route) - 1):
                    from_node = route[i]
                    to_node = route[i+1]
                    segment_distance = aco.distances[from_node][to_node]
                    route_info['total_distance'] += segment_distance
                
                # Construir detalles de cada parada
                for node_idx in route:
                    if node_idx == 0:  # Depósito
                        route_info['stops'].append({
                            'type': 'depot',
                            'location': [depot_lat, depot_lng]
                        })
                    else:
                        node_data = nodes[node_idx]
                        order_idx = (node_idx - 1) // 2  # Índice de la orden
                        order = orders[order_idx] if order_idx < len(orders) else None
                        
                        stop_info = {
                            'type': node_data[0],
                            'location': [node_data[1], node_data[2]],
                            'demand': node_data[3]
                        }
                        
                        if order:
                            stop_info['order_id'] = order.id
                            stop_info['customer'] = order.customer
                        
                        route_info['stops'].append(stop_info)
                
                result['routes'].append(route_info)
            
            return JsonResponse(result, safe=False)
        
        except Exception as e:
            return JsonResponse({'error': str(e), 'type': type(e).__name__}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)