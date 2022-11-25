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
    
def bordeaux(request):
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

    df_room=df_bordeaux[['room_type','amenities']]
    for i in range(df_room.shape[0]):
        A=df_room['amenities'][i]
        df_room['amenities'][i]=len(A.split(','))
    df_room['amenities']=df_room['amenities'].astype(float)
    df_room_mean=df_room.groupby('room_type').describe()
    #Q3=pd.DataFrame({'mean':df_room_mean.iloc[:,1],'std':df_room_mean.iloc[:,2]})
    Q3=df_room_mean.iloc[:,[1,2]].to_html()
    
    #Q4
    df_price=df_bordeaux[['room_type','price']]
    df_price['price']=df_price['price'].str.replace('$','')
    df_price['price']=df_price['price'].str.replace(',','')
    df_price['price']=df_price['price'].astype(float)
    df_price_describe=df_price.groupby('room_type').describe()
    Q4=df_price_describe.iloc[:,[3,4,6,7]].to_html()
    #Q5 

    #Q6


    context={'Q1':Q1,'porcent_phone':porcent_phone, 'porcent_email':porcent_email,'porcent_email_work':porcent_email_work, 'Q3':Q3,'Q4':Q4}
    return render(request, 'afficharge/result.html', context=context)
