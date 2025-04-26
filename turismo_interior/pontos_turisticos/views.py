from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.db.models import Count, Avg
from .models import TouristSpot, Type, CityType
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.

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
            queryset = queryset.filter(city=city)
        
        # Filtro por tipo
        type_name = self.request.GET.get('type')
        if type_name and type_name != 'Todos':
            queryset = queryset.filter(types__name=type_name)
        
        return queryset.select_related().prefetch_related('types').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicionar lista de cidades únicas
        context['cities'] = ['Todas'] + list(
            TouristSpot.objects.values_list('city', flat=True)
            .distinct()
            .order_by('city')
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

class StatisticsView(TemplateView):
    template_name = 'pontos_turisticos/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas gerais
        context['total_spots'] = TouristSpot.objects.count()
        context['total_cities'] = TouristSpot.objects.values('city').distinct().count()
        context['avg_rating'] = TouristSpot.objects.aggregate(Avg('rating'))['rating__avg']
        
        # Top 10 cidades com mais pontos turísticos
        context['top_cities'] = (
            TouristSpot.objects.values('city')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        
        # Distribuição por tipo
        context['type_distribution'] = (
            Type.objects.annotate(count=Count('touristspot'))
            .values('name', 'count')
            .order_by('-count')
        )
        
        return context

def list_spots(request):
    # Obtém parâmetros de filtro
    city = request.GET.get('city', 'Todas')
    type = request.GET.get('type', 'Todos')
    
    # Obtém todos os spots
    spots = TouristSpot.objects.all()
    
    # Aplica filtros
    if city != 'Todas':
        spots = spots.filter(city=city)
    if type != 'Todos':
        spots = spots.filter(types__name=type)
    
    # Obtém cidades e tipos únicos para os filtros
    cities = ['Todas'] + list(TouristSpot.objects.values_list('city', flat=True).distinct())
    types = ['Todos'] + list(TouristSpot.objects.values_list('types__name', flat=True).distinct())
    
    # Paginação
    paginator = Paginator(spots, 9)  # 9 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'spots': page_obj,
        'cities': cities,
        'types': types,
        'current_city': city,
        'current_type': type,
        'is_paginated': page_obj.has_other_pages()
    }
    
    return render(request, 'pontos_turisticos/list.html', context)

def get_types_for_city(request):
    city = request.GET.get('city', '')
    print(f"Buscando tipos para a cidade: {city}")  # Debug
    
    if city == 'Todas':
        # Se for 'Todas', retorna todos os tipos únicos da tabela CityType
        types = CityType.objects.values_list('type', flat=True).distinct()
    else:
        # Para uma cidade específica, busca os tipos diretamente da tabela CityType
        types = CityType.objects.filter(city=city).values_list('type', flat=True)
    
    # Converte para lista e remove valores None
    types_list = list(filter(None, types))
    print(f"Tipos encontrados: {types_list}")  # Debug
    
    return JsonResponse(types_list, safe=False)
