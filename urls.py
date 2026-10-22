"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from app.views import dashboard, entrar, detalhes_campanha, criar_campanha, deletar_campanha, editar_campanha, criar_ficha, ver_ficha, editar_ficha, deletar_ficha, sair

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('entrar/', entrar, name='entrar'),
    path('detalhes_campanha/<int:id>/', detalhes_campanha, name='detalhes_campanha'),
    path('criar_campanha/', criar_campanha, name='criar_campanha'),
    path('deletar_campanha/<int:id>/', deletar_campanha, name='deletar_campanha'),
    path('editar_campanha/<int:id>/', editar_campanha, name='editar_campanha'),
    path('criar_ficha/<int:id>/', criar_ficha, name='criar_ficha'),
    path('ver_ficha/<int:id>/', ver_ficha, name='ver_ficha'),
    path('editar_ficha/<int:id>/', editar_ficha, name='editar_ficha'),
    path('deletar_ficha/<int:id>/', deletar_ficha, name='deletar_ficha'),
    path('sair/', sair, name='sair'),
]
