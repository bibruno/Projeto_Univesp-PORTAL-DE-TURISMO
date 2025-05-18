from django.views.generic import ListView, TemplateView
from django.http import JsonResponse
from django.db.models import Count
from .models import TouristSpot, City, Type
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

def get_types_for_city(request):
    city = request.GET.get('city', '')
    logger.debug(f"API chamada com cidade: {city}")
    print(f"API chamada - Buscando tipos para a cidade: {city}")  # Debug
    
    if city == 'Todas':
        # Se for 'Todas', retorna todos os tipos únicos
        types = Type.objects.values_list('name', flat=True).distinct()
    else:
        # Para uma cidade específica, tenta uma busca mais flexível
        queryset = Type.objects.filter(touristspot__city__name=city)
        
        # Se não encontrar resultados, tenta uma busca com contains
        if not queryset.exists():
            city_base = city.split(',')[0].strip() if ',' in city else city
            queryset = Type.objects.filter(touristspot__city__name__contains=city_base)
            print(f"Tentando busca flexível para: {city_base}")
            
            # Se ainda não encontrar, lista todas as cidades disponíveis para debug
            if not queryset.exists():
                all_cities = list(City.objects.values_list('name', flat=True).distinct()[:20])
                print(f"Cidades disponíveis (primeiras 20): {all_cities}")
        
        print(f"Query SQL: {str(queryset.query)}")
        types = queryset.values_list('name', flat=True).distinct()
    
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