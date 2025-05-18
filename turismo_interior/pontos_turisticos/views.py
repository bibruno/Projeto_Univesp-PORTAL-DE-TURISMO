from django.views.generic import ListView, TemplateView
from django.http import JsonResponse
from django.db.models import Count
from .models import TouristSpot, City, Type, CityType

def get_types_for_city(request):
    city = request.GET.get('city', '')
    print(f"Buscando tipos para a cidade: {city}")  # Debug
    
    if city == 'Todas':
        # Se for 'Todas', retorna todos os tipos únicos
        types = Type.objects.values_list('name', flat=True).distinct()
    else:
        # Para uma cidade específica, busca os tipos da tabela CityType
        types = CityType.objects.filter(
            city__name=city
        ).values_list('type', flat=True).distinct()
    
    # Converte para lista e remove valores None
    types_list = list(filter(None, types))
    print(f"Tipos encontrados: {types_list}")  # Debug
    
    return JsonResponse(types_list, safe=False)

class TouristSpotListView(ListView):
    model = TouristSpot
    template_name = 'pontos_turisticos/list.html'
    context_object_name = 'spots'
    paginate_by = 9

    def get_queryset(self):
        queryset = TouristSpot.objects.all()
        
        # Filtro por cidade
        city = self.request.GET.get('city')
        if city and city != 'Todas':
            queryset = queryset.filter(city__name=city)
        
        # Filtro por tipo
        type_name = self.request.GET.get('type')
        if type_name and type_name != 'Todos':
            queryset = queryset.filter(types__name=type_name)
        
        return queryset.select_related('city').prefetch_related('types').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicionar lista de cidades únicas
        context['cities'] = ['Todas'] + list(
            City.objects.values_list('name', flat=True)
            .distinct()
            .order_by('name')
        )
        
        # Adicionar lista de tipos
        context['types'] = ['Todos'] + list(
            Type.objects.annotate(count=Count('touristspot'))
            .values_list('name', flat=True)
            .order_by('name')
        )
        
        # Adicionar filtros atuais
        context['current_city'] = self.request.GET.get('city', 'Todas')
        context['current_type'] = self.request.GET.get('type', 'Todos')
        
        return context 