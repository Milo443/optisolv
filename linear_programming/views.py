from django.shortcuts import render
import json
import numpy as np
import re

# =================================================================
#                         HELPERS MATEMÁTICOS
# =================================================================

def parse_linear_equation(eq_str):
    """
    Parsea una restricción en coeficientes y sentido (sense).
    Ejemplo: "5*x1 + 8*x2 <= 1000" -> (5.0, 8.0, '<=', 1000.0)
    """
    
    # Expresión regular para manejar coeficientes opcionales (ej: x1 o -x2)
    # Patrón: (coef_x1)x1 (coef_x2)x2 (sense) (b)
    pattern = r'([\d\.\-\+]*)?\*?x1\s*([\+\-][\d\.]*)?\*?x2\s*(<=|>=|=)\s*(\d+\.?\d*)'
    match = re.search(pattern, eq_str.replace(' ', ''))
    
    if not match:
        raise ValueError(f"Formato de restricción no válido: {eq_str}. Use C1*x1 + C2*x2 <= B.")

    try:
        c1_raw = match.group(1)
        c2_raw = match.group(2)

        # 1. Parsear c1
        if not c1_raw: c1 = 1.0 
        elif c1_raw in ('-', '+'): c1 = float(c1_raw + '1')
        else: c1 = float(c1_raw.replace('*', ''))

        # 2. Parsear c2
        if not c2_raw: c2 = 0.0
        elif c2_raw in ('-', '+'): c2 = float(c2_raw + '1')
        else: c2 = float(c2_raw.replace('*', ''))
        
        sense = match.group(3)
        b = float(match.group(4))
        
    except ValueError:
        raise ValueError("Error de conversión: Coeficientes o el lado derecho (B) no son números válidos.")
    
    return c1, c2, sense, b

def check_feasibility(point, constraints):
    """Verifica si un punto (x1, x2) satisface TODAS las restricciones (incluyendo no negatividad)."""
    x1, x2 = point
    TOLERANCE = 1e-6 
    
    # No negatividad
    if x1 < -TOLERANCE or x2 < -TOLERANCE:
        return False
        
    for c1, c2, sense, b in constraints:
        value = c1 * x1 + c2 * x2
        
        if sense == '<=' and value > b + TOLERANCE: 
            return False
        if sense == '>=' and value < b - TOLERANCE: 
            return False
        if sense == '=' and abs(value - b) > TOLERANCE: 
             return False
             
    return True

# =================================================================
#                             VISTAS
# =================================================================

def graphical_method_view(request):
    results = None
    chart_data = None
    
    # Diccionario para retener los datos de entrada del formulario
    input_data = {
        'objective_type': 'MAX',
        'objective_func': '',
        'restrictions': [] # Lista de strings de restricciones
    } 

    if request.method == 'POST':
        
        objective_type = request.POST.get('objective_type', 'MAX')
        objective_func_str = request.POST.get('objective_func', '')
        
        # 1. Retener los datos de entrada
        input_data['objective_type'] = objective_type
        input_data['objective_func'] = objective_func_str
        
        raw_restrictions = []
        for key in sorted(request.POST.keys()): 
            if key.startswith('restriction_') and request.POST[key]:
                raw_restrictions.append(request.POST[key])

        input_data['restrictions'] = raw_restrictions
        
        try:
            
            # 2. Parsing y Preparación Matemática
            
            # 2.1. Parsear la función objetivo
            obj_match = re.search(r'([\d\.\-\+]*)?\*?x1\s*([\+\-][\d\.]*)?\*?x2', objective_func_str.replace(' ', ''))
            if obj_match:
                c1_raw = obj_match.group(1)
                c2_raw = obj_match.group(2)
                
                if not c1_raw: c1_obj = 1.0 
                elif c1_raw in ('-', '+'): c1_obj = float(c1_raw + '1')
                else: c1_obj = float(c1_raw.replace('*', ''))
                
                if not c2_raw: c2_obj = 0.0
                elif c2_raw in ('-', '+'): c2_obj = float(c2_raw + '1')
                else: c2_obj = float(c2_raw.replace('*', ''))
                
                obj_coeffs = (c1_obj, c2_obj)
            else:
                raise ValueError("Formato de Función Objetivo no válido. Use C1*x1 + C2*x2.")


            # 2.2. Parsear restricciones
            parsed_constraints = []
            for value in raw_restrictions:
                c1, c2, sense, b = parse_linear_equation(value)
                parsed_constraints.append((c1, c2, sense, b, value))
            
            if not parsed_constraints:
                raise ValueError("Debe ingresar al menos una restricción estructural.")

            # 2.3. Lista completa de restricciones (incluye no negatividad)
            all_constraints_for_check = [c[:4] for c in parsed_constraints]
            all_constraints_for_check.extend([(1, 0, '>=', 0), (0, 1, '>=', 0)])
            
            
            # 3. Encontrar Puntos de Intersección y Vértices Factibles
            
            A_lines = [(c[0], c[1], c[3], c[4]) for c in parsed_constraints]
            A_lines.extend([(1, 0, 0, 'Eje x2 (x1=0)'), (0, 1, 0, 'Eje x1 (x2=0)')])
            
            intersection_points = set()
            max_coord = 50.0 

            for i in range(len(A_lines)):
                for j in range(i + 1, len(A_lines)):
                    c1_i, c2_i, b_i, _ = A_lines[i]
                    c1_j, c2_j, b_j, _ = A_lines[j]
                    
                    A = np.array([[c1_i, c2_i], [c1_j, c2_j]])
                    b = np.array([b_i, b_j])
                    
                    try:
                        solution = np.linalg.solve(A, b)
                        point = tuple(np.round(solution, 6))
                        
                        if point[0] >= 0 and point[1] >= 0:
                            max_coord = max(max_coord, point[0] * 1.2, point[1] * 1.2)
                            
                        intersection_points.add(point)
                        
                    except np.linalg.LinAlgError:
                        continue 


            # 4. Evaluación y Óptimo
            feasible_vertices = []
            optimal_value = None
            optimal_point = None
            c1_obj, c2_obj = obj_coeffs

            for point in intersection_points:
                if check_feasibility(point, all_constraints_for_check):
                    x1, x2 = point
                    Z = c1_obj * x1 + c2_obj * x2
                    
                    if optimal_value is None:
                        optimal_value = Z
                        optimal_point = point
                    elif objective_type == 'MAX' and Z > optimal_value + 1e-6:
                        optimal_value = Z
                        optimal_point = point
                    elif objective_type == 'MIN' and Z < optimal_value - 1e-6:
                        optimal_value = Z
                        optimal_point = point
                        
                    feasible_vertices.append({
                        'Punto': f'V{len(feasible_vertices) + 1}',
                        'X1': x1,
                        'X2': x2,
                        'Z': Z
                    })
            
            if not feasible_vertices:
                 raise ValueError("La región factible es vacía (problema inconsistente) o el problema no está acotado.")
                 
            # Marcar el óptimo
            for vertex in feasible_vertices:
                is_optimal = (abs(vertex['Z'] - optimal_value) < 1e-6)
                vertex['is_optimal'] = is_optimal
                
            # --- 5. Preparación de Datos para el Gráfico ---
            
            chart_lines = []
            
            for c1, c2, sense, b, label in parsed_constraints:
                x_intercept = b / c1 if abs(c1) > 1e-9 else 0
                y_intercept = b / c2 if abs(c2) > 1e-9 else 0
                
                points = []
                if abs(c1) < 1e-9: 
                    points = [{'x': 0, 'y': y_intercept}, {'x': max_coord, 'y': y_intercept}]
                elif abs(c2) < 1e-9: 
                    points = [{'x': x_intercept, 'y': 0}, {'x': x_intercept, 'y': max_coord}]
                else: 
                    points = [{'x': 0, 'y': y_intercept}, {'x': x_intercept, 'y': 0}]
                
                chart_lines.append({
                    'label': label,
                    'data': points,
                    'color': f'hsl({np.random.randint(0, 360)}, 70%, 50%)' 
                })
                
            chart_lines.append({'label': 'x1 >= 0', 'data': [{'x': 0, 'y': 0}, {'x': max_coord, 'y': 0}], 'color': 'rgba(0, 0, 0, 0.4)'})
            chart_lines.append({'label': 'x2 >= 0', 'data': [{'x': 0, 'y': 0}, {'x': 0, 'y': max_coord}], 'color': 'rgba(0, 0, 0, 0.4)'})

            region_vertices = [(v['X1'], v['X2']) for v in feasible_vertices]
            
            chart_data = {
                'lines': chart_lines,
                'region_vertices': region_vertices,
                'max_scale': max_coord 
            }
            
            results = {
                'optimal_point': optimal_point,
                'optimal_value': optimal_value,
                'vertices': feasible_vertices
            }

        except ValueError as e:
            results = {'error': str(e)}
        except Exception as e:
            results = {'error': f"Ocurrió un error inesperado en el cálculo. Error: {type(e).__name__}: {str(e)}"}
            
    # 🌟 Solución al JSON: Serializar restricciones para inyección segura
    restrictions_json = json.dumps(input_data['restrictions'])

    context = {
        'results': results,
        'chart_data_json': json.dumps(chart_data) if chart_data else 'null',
        'input_data': input_data,
        'restrictions_json': restrictions_json, # <-- ¡VARIABLE CLAVE!
    }
    return render(request, 'linear_programming/graphical_method.html', context)
# Vistas Placeholder
def simplex_method_placeholder(request):
    context = {'method_name': 'Método Simplex'}
    return render(request, 'linear_programming/placeholder.html', context)

def two_phase_method_placeholder(request):
    context = {'method_name': 'Método de las Dos Fases'}
    return render(request, 'linear_programming/placeholder.html', context)