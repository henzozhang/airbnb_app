from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('signup/', views.UserCreateView.as_view(), name='signup')
    # path('about/', views.about_view, name='about'),
    # path('bordeaux/', views.bordeaux, name='bordeaux'),
    # path('lyon/', views.lyon,  name='lyon'),
    # path('paris/', views.paris, name='paris'),
    # path('pays-basque/', views.pays_basque,  name='pays-basque')
#     accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
]
