from django_filters import rest_framework as filters
from .models import Especialidade, Medico, Agenda


class EspecialidadeFilter(filters.FilterSet):
    search = filters.CharFilter(field_name="nome", lookup_expr='icontains')

    class Meta:
        model = Especialidade
        fields = ['search']


class MedicoFilter(filters.FilterSet):
    search = filters.CharFilter(field_name="nome", lookup_expr='icontains')
    especialidade = filters.ModelMultipleChoiceFilter(
        queryset=Especialidade.objects.all()
    )

    class Meta:
        model = Medico
        fields = ['search', 'especialidade']


class AgendaFilter(filters.FilterSet):
    medico = filters.ModelMultipleChoiceFilter(
        queryset=Medico.objects.all()
    )
    especialidade = filters.ModelMultipleChoiceFilter(
        field_name='medico__especialidade',
        lookup_expr='exact',
        queryset=Especialidade.objects.all()
    )
    data_inicio = filters.CharFilter(field_name="dia", lookup_expr='gte')
    data_final = filters.CharFilter(field_name="dia", lookup_expr='lte')

    class Meta:
        model = Agenda
        fields = ['medico', 'especialidade', 'data_inicio', 'data_final']
