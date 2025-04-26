from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.db.models import Count, Avg
from .models import TouristSpot, Type

# Create your views here.

class TouristSpotListView(ListView):
    model = TouristSpot
    template_name = 'pontos_turisticos/list.html'
    context_object_name = 'spots'
    paginate_by = 20

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
        
        return queryset.select_related().prefetch_related('types')

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
