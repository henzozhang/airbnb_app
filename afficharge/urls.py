from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home')
    # path('about/', views.about_view, name='about'),
    # path('bordeaux/', views.bordeaux, name='bordeaux'),
    # path('lyon/', views.lyon,  name='lyon'),
    # path('paris/', views.paris, name='paris'),
    # path('pays-basque/', views.pays_basque,  name='pays-basque')
]
