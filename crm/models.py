
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Campaigns(models.Model):
    id_estado = models.IntegerField()
    codigo = models.CharField(unique=True, max_length=16)
    nombre = models.CharField(max_length=64)
    descripcion = models.TextField()
    brokers = models.TextField()
    fc_inicio = models.IntegerField()
    fc_final = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'campaigns'


class CampaignsEstados(models.Model):
    nombre = models.CharField(max_length=32)
    descripcion = models.TextField()

    class Meta:
        managed = False
        db_table = 'campaigns_estados'


class Contactos(models.Model):
    id_estado = models.IntegerField()
    id_domicilio = models.PositiveIntegerField()
    id_ocupacion = models.IntegerField()
    id_estado_civil = models.IntegerField()
    ci = models.BigIntegerField()
    nombre1 = models.CharField(max_length=32)
    nombre2 = models.CharField(max_length=32)
    apellido1 = models.CharField(max_length=32)
    apellido2 = models.CharField(max_length=32)
    fc_nacimiento = models.IntegerField()
    sexo = models.CharField(max_length=1)
    zurdo = models.CharField(max_length=1)
    id_tel_fijo1 = models.IntegerField()
    id_tel_fijo2 = models.IntegerField()
    id_tel_movil1 = models.IntegerField()
    id_tel_movil2 = models.IntegerField()
    email = models.TextField()
    id_userinsert = models.IntegerField()
    id_fuente_dato = models.IntegerField()
    se_queda = models.IntegerField()
    timestamp = models.BigIntegerField()
    lastupdate = models.DateTimeField()
    mascota = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contactos'


class ContactosEstado(models.Model):
    nombre = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'contactos_estado'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Gestiones(models.Model):
    id_tipo = models.IntegerField()
    id_campaign = models.IntegerField()
    id_broker = models.IntegerField()
    id_contacto = models.IntegerField()
    id_resultado = models.IntegerField()
    notas = models.TextField()
    timestamp = models.CharField(max_length=14)
    id_tel_fijo1 = models.IntegerField()
    lastupdate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'gestiones'


class GestionesResultado(models.Model):
    nombre = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'gestiones_resultado'


class GestionesTipo(models.Model):
    nombre = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'gestiones_tipo'


class Telefonos(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.IntegerField()
    numero = models.PositiveBigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'telefonos'


class Users(models.Model):
    id_tipo = models.IntegerField()
    id_estado = models.IntegerField()
    id_grupo = models.IntegerField()
    id_categoria = models.IntegerField()
    ci = models.IntegerField()
    nombre = models.CharField(max_length=32)
    apellido = models.CharField(max_length=32)
    usuario = models.CharField(max_length=32)
    password = models.TextField()
    id_tipo_escala = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'


class UsersCategorias(models.Model):
    categoria = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'users_categorias'


class UsersEstados(models.Model):
    nombre = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'users_estados'


class UsersGrupos(models.Model):
    nombre = models.CharField(max_length=32)
    descripcion = models.TextField()

    class Meta:
        managed = False
        db_table = 'users_grupos'


class UsersTipos(models.Model):
    nombre = models.CharField(max_length=32)
    descripcion = models.TextField()

    class Meta:
        managed = False
        db_table = 'users_tipos'


#tabla para los snapshots:
class DashboardSnapshot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # fecha de creación automática
    contactabilidad = models.FloatField()                # valor de KPI calculado
    penetracion_bruta = models.FloatField()             # valor de KPI calculado
    penetracion_neta = models.FloatField()              # valor de KPI calculado
    filtros = models.JSONField()                        # guarda filtros como {id_agente, id_campania, fechas}


    def __str__(self):
        return f"Snapshot {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"