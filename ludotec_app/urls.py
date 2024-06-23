"""
URL configuration for Proyecto_Jaime project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add, name='add'),
    path('query/', views.query, name='query'),
    path('register/', views.register, name='register'),
    path('statistics/', views.statistics, name='statistics'),
    path('query/detalle_juego/<int:juego_id>/', views.detalle_juego, name='detalle_juego'),
    path('borrar_juego/<int:juego_id>/', views.borrar_juego, name='borrar_juego'),
    path('query/detalle_juego/<int:juego_id>/boardgame_statistic/', views.boardgame_statistic, name='boardgame_statistic'),
    path('feedback/', views.feedback, name='feedback'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

