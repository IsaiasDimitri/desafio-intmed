from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
from django.core.validators import MaxValueValidator


class User(AbstractUser):
    username = models.CharField(_("username"), max_length=255, unique=True)
    email = models.EmailField(_("email"), max_length=255, null=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)

    USERNAME_FIELD = "username"
    objects = UserManager()


class Especialidade(models.Model):
    nome = models.CharField("especialidade", max_length=100, null=False, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(
        "nome",
        max_length=55,
        blank=False,
        null=False,
    )
    crm = models.IntegerField(
        "crm",
        blank=False,
        null=False,
        validators=[MaxValueValidator(99999)],
    )
    email = models.EmailField(
        "email",
        max_length=100,
        null=False,
    )
    telefone = models.CharField(
        "telefone",
        max_length=15,
    )
    especialidade = models.ForeignKey(
        Especialidade,
        default=None,
        on_delete=models.SET_DEFAULT,
    )

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]


class Agenda(models.Model):
    medico = models.ForeignKey(
        Medico,
        related_name="agenda",
        on_delete=models.CASCADE,
    )
    dia = models.DateField(
        "dia",
        blank=False,
        null=False,
    )
    horarios = ArrayField(
        models.TimeField("Horários"),
    )

    def __str__(self):
        return f"{self.medico} - dia: {self.dia}"

    class Meta:
        ordering = ["dia"]


class Consulta(models.Model):
    data_agendamento = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )  # paciente
    agenda = models.ForeignKey(
        Agenda,
        on_delete=models.CASCADE,
    )
    horario = models.TimeField(
        "horarios",
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"{self.agenda.dia} - {self.horario} - {self.agenda.medico.nome}"

    class Meta:
        ordering = ["owner"]
