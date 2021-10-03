from django.db.models.query import QuerySet
from .models import User, Agenda, Consulta, Medico, Especialidade
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = "__all__"


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = serializers.SerializerMethodField()

    def get_especialidade(self, obj):
        return EspecialidadeSerializer(
            Especialidade.objects.filter(id=obj.especialidade.id).first(),
        ).data

    class Meta:
        model = Medico
        fields = [
            "id",
            "nome",
            "crm",
            "email",
            "telefone",
            "especialidade",
        ]


class AgendaSerializer(serializers.ModelSerializer):
    medico = serializers.SerializerMethodField()
    horarios = serializers.SerializerMethodField()
    dia = serializers.SerializerMethodField()

    def get_medico(self, obj):
        return MedicoSerializer(
            Medico.objects.filter(id=obj.medico.id).first(),
        ).data
    
    def get_horarios(self, obj):
        return obj.horarios
    
    def get_dia(self, obj):
        return obj.dia

    class Meta:
        model = Agenda
        depth = 3
        fields = [
            "id",
            "medico",
            "dia",
            "horarios",
        ]


class ConsultaSerializer(serializers.ModelSerializer):
    dia = serializers.SerializerMethodField()
    medico = serializers.SerializerMethodField()
    agenda_id = serializers.PrimaryKeyRelatedField(queryset=Agenda.objects.all())

    def get_dia(self, obj):
        return obj.agenda.dia

    def get_medico(self, obj):
        return MedicoSerializer(
            Medico.objects.filter(id=obj.agenda.medico.id).first(),
            read_only=True,
        ).data

    class Meta:
        model = Consulta
        fields = [
            "id",
            "dia",
            "medico",
            "agenda_id",
            "horario",
        ]
