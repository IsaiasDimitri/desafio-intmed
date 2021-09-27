from .models import User, Agenda, Consulta, Medico, Especialidade
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]

    extra_kwargs = {"password": {"write_only": True, "required": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = "__all__"


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = serializers.PrimaryKeyRelatedField(
        queryset=Especialidade.objects.all()
    )

    class Meta:
        model = Medico
        depth = 2
        fields = [
            'id',
            'nome',
            'crm',
            'email',
            'telefone',
            'especialidade'
        ]


class AgendaSerializer(serializers.ModelSerializer):
    medico = serializers.PrimaryKeyRelatedField(queryset=Medico.objects.all())

    class Meta:
        model = Agenda
        depth = 2
        fields = ["id", "medico", "dia", "horarios"]


class ConsultaSerializer(serializers.ModelSerializer):
    dia = serializers.SerializerMethodField()
    medico = serializers.SerializerMethodField()

    def get_agenda(self, obj):
        return obj.agenda.dia

    def get_medico(self, obj):
        return MedicoSerializer(Medico.objects.filter(
            id=obj.agenda.medico).first(), read_only=True).data


    class Meta:
        model = Consulta
        depth = 2
        fields = ["id", "dia", "horario", "data_agendamento"]
