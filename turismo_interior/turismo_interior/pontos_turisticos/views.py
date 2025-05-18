from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.db.models import Count, Avg
from .models import TouristSpot, Type, CityType
from django.core.paginator import Paginator
from django.http import JsonResponse
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

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
            # Remove o sufixo ", SP" se existir
            city_name = city.replace(', SP', '')
            queryset = queryset.filter(city__icontains=city_name)
        
        # Filtro por tipo
        type_name = self.request.GET.get('type')
        if type_name and type_name != 'Todos':
            queryset = queryset.filter(types__name__iexact=type_name)
        
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
    logger.debug(f"API chamada com cidade: {city}")
    
    if not city or city == 'Todas':
        # Se não houver cidade selecionada ou for 'Todas', retorna todos os tipos
        types = Type.objects.values_list('name', flat=True).distinct()
        logger.debug("Retornando todos os tipos disponíveis")
    else:
        # Remove o sufixo ", SP" se existir
        city_name = city.replace(', SP', '')
        logger.debug(f"Buscando tipos para cidade: {city_name}")
        
        # Verifica se existem pontos turísticos para a cidade
        spots = TouristSpot.objects.filter(city__icontains=city_name)
        logger.debug(f"Pontos turísticos encontrados: {spots.count()}")
        
        # Lista os pontos encontrados e seus tipos
        for spot in spots:
            logger.debug(f"Ponto: {spot.name}, Cidade: {spot.city}, Tipos: {[t.name for t in spot.types.all()]}")
        
        # Busca tipos diretamente da relação many-to-many
        types = Type.objects.filter(
            touristspot__city__icontains=city_name
        ).distinct()
        
        # Lista todos os tipos encontrados com contagem
        for type_obj in types:
            count = type_obj.touristspot_set.filter(city__icontains=city_name).count()
            logger.debug(f"Tipo '{type_obj.name}' tem {count} pontos turísticos em {city_name}")
        
        # Converte para lista de nomes
        types = types.values_list('name', flat=True)
        logger.debug(f"Tipos encontrados (busca exata): {list(types)}")
        
        # Se não encontrar nenhum tipo, tenta uma busca mais flexível
        if not types:
            logger.debug("Tentando busca flexível...")
            # Primeiro tenta sem o sufixo SP
            types = Type.objects.filter(
                touristspot__city__icontains=city_name.replace(', SP', '')
            ).values_list('name', flat=True).distinct()
            
            # Se ainda não encontrar, tenta com a primeira palavra
            if not types:
                first_word = city_name.split()[0]
                logger.debug(f"Buscando com primeira palavra: {first_word}")
                types = Type.objects.filter(
                    touristspot__city__icontains=first_word
                ).values_list('name', flat=True).distinct()
                
                if not types:
                    # Tenta uma busca case-insensitive no nome da cidade
                    logger.debug("Tentando busca case-insensitive")
                    types = Type.objects.filter(
                        touristspot__city__iexact=city_name
                    ).values_list('name', flat=True).distinct()
    
    types_list = list(types)
    logger.debug(f"Tipos finais encontrados para {city}: {types_list}")
    return JsonResponse(types_list, safe=False)
