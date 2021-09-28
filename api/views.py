from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from .models import (
    Agenda,
    Consulta,
    Especialidade,
    Medico,
    User,
)
from .serializers import (
    UserSerializer,
    AgendaSerializer,
    ConsultaSerializer,
    EspecialidadeSerializer,
    MedicoSerializer,
)
import datetime
import time

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = User.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_staff=False)
        return queryset

    def create(self, request, *args, **kwargs):
        super(UserViewSet, self).create(request, *args, **kwargs)
        return Response(
            {"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        print(request.user.is_superuser)
        if not request.user.is_superuser:
            return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(UserViewSet, self).update(request, *args, **kwargs)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response({"token": token.key})


class EspecialidadeViewSet(viewsets.ModelViewSet):
    serializer_class = EspecialidadeSerializer

    def get_queryset(self):
        queryset = Especialidade.objects.all()
        search = self.request.query_params.get("search")
        if search is not None:
            queryset = queryset.filter(nome__contains=search)
        return queryset


class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

    def get_queryset(self):
        queryset = Medico.objects.all()
        search = self.request.query_params.get("search")
        if search is not None:
            queryset = queryset.filter(nome__contains=search)

        especialidade = self.request.query_params.get("especialidade")
        if especialidade is not None:
            especialidade = self.request.query_params.getlist("especialidade")
            queryset = queryset.filter(especialidade__in=especialidade)
        return queryset


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    def get_queryset(self):
        today = datetime.date.today()
        queryset = self.queryset.filter(dia__gte=today, horarios__len__gt=0)
        time_now = time.strftime("%H:%M:%S")
        for agenda in queryset:
            for horario in agenda.horarios:
                if time_now > str(horario) and today >= agenda.dia:
                    agenda.horarios.remove(horario)
                    agenda.save()
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(AgendaViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        print(request.user.is_superuser)
        if not request.user.is_superuser:
            return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(AgendaViewSet, self).list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(dict(status=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(AgendaViewSet, self).update(request, *args, **kwargs)


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

    def get_queryset(self):
        date_now = datetime.date.today()
        time_now = time.strftime("%H:%M:%S")

        queryset = Consulta.objects.filter(
            agenda__dia__gte=date_now, owner=self.request.user
        )
        queryset = queryset.order_by("agenda__dia", "horario")
        return queryset.exclude(agenda__dia__exact=date_now, horario__lte=time_now)

    def create(self, request, *args, **kwargs):
        consulta = Consulta()
        consulta.owner = request.user
        try:
            agenda = Agenda.objects.get(pk=request.data.get("agenda"))
        except Agenda.DoesNotExist as e:
            error = dict(status=400, error={"message": str(e)})
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        horario = request.data.get("horario")

        try:
            time.strptime(horario, "%H:%M")
        except ValueError:
            error = dict(
                status=400,
                error={
                    "message": f"{horario} tem um formato inválido. Deve estar no formato HH:MM."
                },
            )
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        date_now, time_now = datetime.date.today(), time.strftime("%H:%M")
        if agenda.dia < date_now or (
            agenda.dia == date_now and str(horario) < time_now
        ):
            error = dict(
                status=400,
                error={
                    "message": "Não é possível marcar uma consulta em um tempo passado!"
                },
            )
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        for hora in agenda.horarios:
            if str(hora.strftime("%H:%M")) == horario:
                if Consulta.objects.filter(
                    agenda__dia=agenda.dia, horario=horario
                ).exists():
                    error = dict(
                        status=400,
                        error={
                            "message": "horário indisponível!"
                        },
                    )
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)

                consulta.agenda = agenda
                consulta.horario = horario
                consulta.save()

                agenda_horario = Agenda.objects.filter(
                    horarios__contains=[horario], id=agenda.id
                )
                if agenda_horario.exists():
                    agenda_obj = agenda_horario.first()
                    agenda_obj.horarios.remove(hora)
                    agenda_obj.save()

                serializer = ConsultaSerializer(consulta)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        error = dict(
            status=400,
            error={
                "message": "erro ao marcar consulta."
            },
        )
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        consulta = Consulta.objects.filter(pk=kwargs.get("pk"), owner=request.user)

        if consulta.exists():
            consulta_marcada = consulta.first()

            today, time_now = datetime.date.today(), time.strftime("%H:%M")
            if consulta_marcada.agenda.dia < today or (
                consulta_marcada.agenda.dia == today
                and str(consulta_marcada.hourly) < time_now
            ):
                error = dict(
                    status=400,
                    error={
                        "message": "Não é possível desmarcar uma consulta que já foi realizada!"
                    },
                )
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            return super().destroy(request, *args, **kwargs)

        error = dict(status=400, error={"message": "Consulta inexistente."})
        return Response(error, status=status.HTTP_404_NOT_FOUND)
