from django.contrib import admin
from .models import Consulta, Especialidade, Agenda, Medico, User
from rest_framework.authtoken.admin import TokenAdmin


admin.register(TokenAdmin)


@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ["nome"]
    list_filter = ["nome"]
    search_fields = ["nome"]


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ["nome", "email", "crm"]
    list_filter = ["nome", "email", "crm", "telefone"]
    search_fields = ["nome", "email", "especialidade"]


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ["medico", "dia"]
    list_filter = ["medico", "dia"]
    search_fields = ["medico", "dia"]


@admin.register(Consulta)
class MedicalAppointmentAdmin(admin.ModelAdmin):
    list_display = ["horario", "agenda"]
    list_filter = ["horario", "agenda"]
    search_fields = ["horario", "agenda"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Acesso", {"fields": ("username", "password")}),
        ("Permissoes", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
