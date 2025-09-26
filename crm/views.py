# crm/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Gestiones, Users, Campaigns, DashboardSnapshot
from .utils import calcular_contactabilidad, calcular_penetracion_bruta, calcular_penetracion_neta

from .utils import supervisor_required


TIPO_LLAMADA = 1
RESULTADOS_EFECTIVOS = [1, 2, 8, 9, 10, 13, 14, 15, 16]
RESULTADOS_EXITOSOS = [1, 8]



@supervisor_required
def dashboard(request):
    # filtros
    id_agente = request.GET.get('id_agente')
    id_campania = request.GET.get('id_campania')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # query base
    gestiones = Gestiones.objects.filter(id_tipo=TIPO_LLAMADA)
    if id_agente:
        gestiones = gestiones.filter(id_broker=id_agente)
    if id_campania:
        gestiones = gestiones.filter(id_campaign=id_campania)
    if fecha_inicio:
        fecha_inicio_str = fecha_inicio.replace('-', '') + '000000'
        gestiones = gestiones.filter(timestamp__gte=fecha_inicio_str)
    if fecha_fin:
        fecha_fin_str = fecha_fin.replace('-', '') + '235959'
        gestiones = gestiones.filter(timestamp__lte=fecha_fin_str)


    contactabilidad = penetracion_bruta = penetracion_neta = 0
    detalle = []
    agentes = Users.objects.all()
    campañas = Campaigns.objects.all()

    if gestiones.exists():
        # KPIs generales
        contactabilidad, _, _ = calcular_contactabilidad(gestiones)
        penetracion_bruta, _ = calcular_penetracion_bruta(gestiones)
        penetracion_neta, _, _ = calcular_penetracion_neta(gestiones)

        # detalle por agente y campaña
        for agente in agentes:
            for camp in campañas:
                g = gestiones.filter(id_broker=agente.id, id_campaign=camp.id)
                if g.exists():
                    total = g.count()
                    efectivas = g.filter(id_resultado__in=RESULTADOS_EFECTIVOS).count()
                    exitosas = g.filter(id_resultado__in=RESULTADOS_EXITOSOS).count()

                    contactabilidad_pct, _, _ = calcular_contactabilidad(g)
                    penetracion_bruta_pct, _ = calcular_penetracion_bruta(g)
                    penetracion_neta_pct, _, _ = calcular_penetracion_neta(g)

                    detalle.append({
                        'agente_nombre': agente.nombre,
                        'campania_nombre': camp.nombre,
                        'total_gestiones': total,
                        'gestiones_efectivas': efectivas,
                        'gestiones_exitosas': exitosas,
                        'contactabilidad': contactabilidad_pct,
                        'penetracion_bruta': penetracion_bruta_pct,
                        'penetracion_neta': penetracion_neta_pct,
                    })

    # contexto para la plantilla
    context = {
        'contactabilidad': contactabilidad,
        'penetracion_bruta': penetracion_bruta,
        'penetracion_neta': penetracion_neta,
        'detalle': detalle,
        'agentes': agentes,
        'campañas': campañas,
        'filtros': {
            'id_agente': id_agente or '',
            'id_campania': id_campania or '',
            'fecha_inicio': fecha_inicio or '',
            'fecha_fin': fecha_fin or '',
        },
        'saved': request.GET.get('saved') == '1',  # para mostrar mensaje
    }

    # guardo snapshot si se recibe el parámetro
    if request.GET.get('save_snapshot') == '1':
        DashboardSnapshot.objects.create(
            contactabilidad=contactabilidad,
            penetracion_bruta=penetracion_bruta,
            penetracion_neta=penetracion_neta,
            filtros={
                'id_agente': id_agente or '',
                'id_campania': id_campania or '',
                'fecha_inicio': fecha_inicio or '-',
                'fecha_fin': fecha_fin or '-',
            }
        )
        # redirigir con saved=1 para mostrar mensaje
        query = request.GET.copy()
        query['saved'] = '1'
        query.pop('save_snapshot', None)
        return redirect(f"{request.path}?{query.urlencode()}")

    return render(request, 'crm/dashboard.html', context)


# ------------------------
# Funciones para snapshots
# ------------------------

 # lista de snapshots realizados
@supervisor_required
def snapshots_list(request):
    snapshots = DashboardSnapshot.objects.order_by('-created_at')
    return render(request, 'crm/snapshots_list.html', {'snapshots': snapshots})


# detalle de snapshot realizados
@supervisor_required
def snapshot_detail(request, snapshot_id):
    snapshot = get_object_or_404(DashboardSnapshot, id=snapshot_id)
    filtros = snapshot.filtros.copy()

    # convertir id_agente a nombre
    id_agente = filtros.get('id_agente')
    if id_agente not in ['', None]:
        try:
            filtros['id_agente'] = Users.objects.get(id=int(id_agente)).nombre
        except (Users.DoesNotExist, ValueError):
            filtros['id_agente'] = f"ID {id_agente}"
    else:
        filtros['id_agente'] = 'Todos'

    # converte id_campania a nombre
    id_campania = filtros.get('id_campania')
    if id_campania not in ['', None]:
        try:
            filtros['id_campania'] = Campaigns.objects.get(id=int(id_campania)).nombre
        except (Campaigns.DoesNotExist, ValueError):
            filtros['id_campania'] = f"ID {id_campania}"
    else:
        filtros['id_campania'] = 'Todas'

    return render(request, 'crm/snapshot_detail.html', {
        'snapshot': snapshot,
        'filtros': filtros,
    })



from django.shortcuts import render, redirect
from .models import Users

def login_supervisor(request):
    mensaje = ""
    if request.method == "POST":
        usuario_input = request.POST.get("usuario")
        password_input = request.POST.get("password")

        try:
            usuario = Users.objects.get(usuario=usuario_input)
            if usuario.password == password_input and usuario.id_tipo == 2:  # 2 = supervisor
                # se guarda info en session
                request.session['user_id'] = usuario.id
                request.session['user_tipo'] = usuario.id_tipo
                request.session['user_nombre'] = usuario.nombre
                return redirect('dashboard')  # redirige al dashboard
            else:
                mensaje = "Usuario o contraseña incorrectos, o no es supervisor."
        except Users.DoesNotExist:
            mensaje = "Usuario no encontrado."

    return render(request, "crm/login_supervisor.html", {"mensaje": mensaje})

def logout_view(request):
    request.session.flush()
    return redirect('login_supervisor')
