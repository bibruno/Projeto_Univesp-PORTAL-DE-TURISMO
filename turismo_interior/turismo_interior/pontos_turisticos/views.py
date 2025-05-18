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
        logger.debug(f"Retornando todos os tipos disponíveis: {list(types)}")
    else:
        # Remove o sufixo ", SP" se existir
        city_name = city.replace(', SP', '')
        logger.debug(f"Buscando tipos para cidade: {city_name}")
        
        # Primeiro, vamos verificar se a cidade existe e como ela está gravada
        all_cities = TouristSpot.objects.values_list('city', flat=True).distinct()
        logger.debug(f"Todas as cidades no banco: {list(all_cities)}")
        
        # Verifica se existem pontos turísticos para a cidade (busca case-insensitive)
        spots = TouristSpot.objects.filter(city__icontains=city_name)
        logger.debug(f"Pontos turísticos encontrados: {spots.count()}")
        
        # Lista os pontos encontrados e seus tipos
        for spot in spots:
            logger.debug(f"Ponto: {spot.name}, Cidade exata: {spot.city}, Tipos: {[t.name for t in spot.types.all()]}")
        
        # Tenta diferentes estratégias de busca
        types = set()  # Usar um set para evitar duplicatas
        
        # 1. Busca exata com cidade completa
        exact_types = Type.objects.filter(
            touristspot__city__iexact=city
        ).values_list('name', flat=True).distinct()
        if exact_types:
            types.update(exact_types)
            logger.debug(f"Tipos encontrados (busca exata com cidade completa): {list(exact_types)}")
        
        # 2. Busca com cidade sem SP
        no_sp_types = Type.objects.filter(
            touristspot__city__iexact=city_name
        ).values_list('name', flat=True).distinct()
        if no_sp_types:
            types.update(no_sp_types)
            logger.debug(f"Tipos encontrados (busca sem SP): {list(no_sp_types)}")
        
        # 3. Busca parcial com icontains
        partial_types = Type.objects.filter(
            touristspot__city__icontains=city_name
        ).values_list('name', flat=True).distinct()
        if partial_types:
            types.update(partial_types)
            logger.debug(f"Tipos encontrados (busca parcial): {list(partial_types)}")
        
        # 4. Se ainda não encontrou nada, tenta com a primeira palavra
        if not types:
            first_word = city_name.split()[0]
            logger.debug(f"Tentando com primeira palavra: {first_word}")
            first_word_types = Type.objects.filter(
                touristspot__city__icontains=first_word
            ).values_list('name', flat=True).distinct()
            if first_word_types:
                types.update(first_word_types)
                logger.debug(f"Tipos encontrados (primeira palavra): {list(first_word_types)}")
        
        # Converte o set para lista
        types_list = list(types)
        
        # Se ainda não encontrou nada, faz uma última verificação
        if not types_list:
            logger.debug("Nenhum tipo encontrado. Verificando pontos turísticos direto:")
            # Verifica se há pontos sem tipos associados
            spots_without_types = TouristSpot.objects.filter(
                city__icontains=city_name,
                types__isnull=True
            ).count()
            logger.debug(f"Pontos sem tipos associados: {spots_without_types}")
            
            # Verifica a contagem total de tipos no sistema
            total_types = Type.objects.count()
            logger.debug(f"Total de tipos no sistema: {total_types}")
            
            # Lista alguns exemplos de pontos e suas cidades para debug
            sample_spots = TouristSpot.objects.filter(
                city__icontains=city_name
            ).values('name', 'city')[:5]
            logger.debug(f"Amostra de pontos encontrados: {list(sample_spots)}")
    
    types_list = list(types) if 'types_list' not in locals() else types_list
    logger.debug(f"Tipos finais encontrados para {city}: {types_list}")
    return JsonResponse(types_list, safe=False)
