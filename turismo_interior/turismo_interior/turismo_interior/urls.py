"""
URL configuration for turismo_interior project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

# Debug do carregamento de URLs
print("Carregando URLs do projeto turismo_interior")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pontos_turisticos.urls')),
]

# Lista todas as URLs para debug
for pattern in urlpatterns:
    print(f"URL registrada: {pattern.pattern}")

print("URLs carregadas com sucesso")
