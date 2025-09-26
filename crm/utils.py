# crm/utils.py
from .models import Gestiones
from django.shortcuts import redirect
from functools import wraps

# resultados que asumo efectivos
RESULTADOS_EFECTIVOS = [1, 2, 8, 9, 10, 13, 14, 15, 16]
# resultados que asumo exitosos
RESULTADOS_EXITOSOS = [1, 8]

def calcular_contactabilidad(gestiones):
    total = gestiones.count()

    contactadas = gestiones.filter(id_resultado__in=RESULTADOS_EFECTIVOS, id_tipo=1).count()
    porcentaje = (contactadas / total) * 100 if total else 0
    return round(porcentaje, 2), total, contactadas


def calcular_penetracion_bruta(gestiones):
    total = gestiones.filter(id_tipo=1).count()  # solo llamadas
    exitosas = gestiones.filter(id_tipo=1, id_resultado__in=RESULTADOS_EXITOSOS).count()
    porcentaje = (exitosas / total) * 100 if total else 0
    return round(porcentaje, 2), exitosas

def calcular_penetracion_neta(gestiones):
    efectivas = gestiones.filter(id_tipo=1, id_resultado__in=RESULTADOS_EFECTIVOS).count()
    exitosas = gestiones.filter(id_tipo=1, id_resultado__in=RESULTADOS_EXITOSOS).count()
    porcentaje = (exitosas / efectivas) * 100 if efectivas else 0
    return round(porcentaje, 2), efectivas, exitosas

def supervisor_required(view_func):
    """
    Decorador para permitir acceso solo a usuarios que sean supervisores.

    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_tipo = request.session.get('user_tipo')
        if user_tipo == 2:  #2 = supervisor
            return view_func(request, *args, **kwargs)
        else:
            # redirige al login si no es supervisor
            return redirect('login_supervisor')
    return _wrapped_view