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
    logger.debug(f"API chamada com cidade: {city}")
    print(f"API chamada - Buscando tipos para a cidade: {city}")  # Debug
    
    # DIAGNÓSTICO DIRETO
    print("\n==== DIAGNÓSTICO DO BANCO DE DADOS ====")
    all_cities = list(TouristSpot.objects.values_list('city', flat=True).distinct()[:20])
    print(f"Cidades disponíveis (primeiras 20): {all_cities}")
    
    all_types = list(Type.objects.values_list('name', flat=True).distinct()[:20])
    print(f"Tipos disponíveis (primeiros 20): {all_types}")
    
    # Verifica se existem pontos turísticos específicos
    amparo_count = TouristSpot.objects.filter(city__icontains='amparo').count()
    print(f"Pontos turísticos com 'amparo' no nome: {amparo_count}")
    
    # Verifica se algum ponto turístico está associado a tipos
    spots_with_types = TouristSpot.objects.filter(types__isnull=False).count()
    print(f"Pontos turísticos que têm tipos associados: {spots_with_types}")
    
    # Verifica qual relação está funcionando
    if amparo_count > 0:
        print("Tentando direto nas relações many-to-many:")
        for spot in TouristSpot.objects.filter(city__icontains='amparo')[:5]:
            types_for_spot = spot.types.all()
            print(f"Spot: {spot.name}, Cidade: {spot.city}, Tipos: {[t.name for t in types_for_spot]}")
    
    print("=== FIM DO DIAGNÓSTICO ===\n")
    
    # RETORNAR SEMPRE TODOS OS TIPOS PARA TESTAR FRONTEND
    # Isso vai fazer o dropdown funcionar com todos os tipos para qualquer cidade
    all_available_types = list(Type.objects.values_list('name', flat=True).distinct())
    print(f"Retornando TODOS os tipos ({len(all_available_types)}) para garantir funcionamento")
    return JsonResponse(all_available_types, safe=False)
