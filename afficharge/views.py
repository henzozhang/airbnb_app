# from django.shortcuts import render

# # Create your views here.
# def home_view(request):
    
#     # import pudb;pu.db()
#     return render(request, 'afficharge/home_page.html')

# def about_view(request):
#     return render(request, 'divers/about_page.html')

from django.shortcuts import render

import pandas as pd
from dotenv import load_dotenv 
load_dotenv()
import os 

def home_page(request):
    return render(request, 'afficharge/home_page.html')
    
def resultat(request):
    #Q1
    df_bordeaux=pd.read_csv('/home/ha-brek/Devia_AI/airbnb_app/Data/listings_bordeaux.csv')
    df_bordeaux_neighbourhood=df_bordeaux[["host_id","number_of_reviews","neighbourhood_cleansed"]].groupby("neighbourhood_cleansed").agg({"host_id":"count","number_of_reviews":"sum"})
    Q1=df_bordeaux_neighbourhood.to_html()

    #Q2
    df_verefication=df_bordeaux[['host_verifications',"host_id"]]

    totale_verification=df_verefication.shape[0]
    number_phone=df_verefication[df_verefication['host_verifications'].str.contains('phone')]['host_verifications'].count()
    porcent_phone=(number_phone/totale_verification)*100
    number_email=df_verefication[df_verefication['host_verifications'].str.contains('email')]['host_verifications'].count()
    porcent_email=(number_email/totale_verification)*100
    number_email_work=df_verefication[df_verefication['host_verifications'].str.contains('work_email')]['host_verifications'].count()
    porcent_email_work=(number_email_work/totale_verification)*100
    #Q3



    context={'Q1':Q1,'porcent_phone':porcent_phone, 'porcent_emai':porcent_email,'porcent_email_work':porcent_email_work}
    return render(request, 'afficharge/result.html', context=context)
