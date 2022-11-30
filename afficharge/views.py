# from django.shortcuts import render

# # Create your views here.
# def home_view(request):
    
#     # import pudb;pu.db()
#     return render(request, 'afficharge/home_page.html')

# def about_view(request):
#     return render(request, 'divers/about_page.html')

from django.shortcuts import render
from .forms import UserCreationFormCustom
from django.views.generic.edit import CreateView
from . import models
# from django.contrib.auth.forms import UserCreationForm
from . import forms
from django.urls import reverse_lazy



import pandas as pd
import numpy as np
from dotenv import load_dotenv 
load_dotenv()
import os 

def home_page(request):
    return render(request, 'afficharge/home_page.html')
    
def bordeaux(request):
    #Q1
    df_bordeaux=pd.read_csv('/home/apprenant/Documents/Data/bordeaux.csv')
    df_bordeaux_reviews=pd.read_csv('/home/apprenant/Documents/Data/bordeaux.csv')
    df_bordeaux_neighbourhood=df_bordeaux[["host_id","number_of_reviews","neighbourhood_cleansed"]].groupby("neighbourhood_cleansed").agg({"host_id":"count","number_of_reviews":"sum"})
    Q1=df_bordeaux_neighbourhood.to_html(justify='left', classes='mystyle')
        

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
    Q3=df_room_mean.iloc[:,[1,2]].to_html(justify='left', classes='mystyle')
    
    #Q4
    df_price=df_bordeaux[['room_type','price']]
    df_price['price']=df_price['price'].str.replace('$','')
    df_price['price']=df_price['price'].str.replace(',','')
    df_price['price']=df_price['price'].astype(float)
    df_price_describe=df_price.groupby('room_type').describe()
    Q4=df_price_describe.iloc[:,[3,4,6,7]].to_html(justify='left', classes='mystyle')
    #Q5 
    temp = (df_bordeaux['bathrooms_text'].str.lower().str.contains('shared') * 0.5)+ (df_bordeaux['bathrooms_text'].str.lower().str.contains('half') * 0.5)
    temp[temp == 1] = 0.25
    temp[temp == 0] = 1
    temp.fillna(1, inplace=True)
    df_bordeaux['bathrooms_cleaned'] = df_bordeaux.bathrooms_text.str.replace(r'[a-zA-Z]', '').str.replace('-', '').str.strip()
    df_bordeaux[df_bordeaux['bathrooms_cleaned'] == ''] = np.nan
    df_bordeaux['bathrooms_cleaned'] = df_bordeaux['bathrooms_cleaned'].astype('float')
    df_bordeaux['bathrooms_cleaned'] = df_bordeaux['bathrooms_cleaned'] * temp
    df_bordeaux['bathrooms_cleaned'].unique()
    Q5=pd.DataFrame({'prix':df_bordeaux['bathrooms_cleaned'].value_counts().sort_index()})
    Q5=Q5.to_html(justify='left', classes='mystyle')
    #Q6
    Q6=df_bordeaux['description'].str.len().corr(df_bordeaux['number_of_reviews'])
    #Q7
    # df_merged_reivews = df_bordeaux[['id', 'host_name']].merge(df_bordeaux_reviews[['listing_id', 'reviewer_name']],left_on='id',right_on='listing_id' )
    # Q7=(df_merged_reivews['host_name'] == df_merged_reivews['reviewer_name']).sum() / len(df_merged_reivews)

    context={'Q1':Q1,'porcent_phone':porcent_phone, 'porcent_email':porcent_email,'porcent_email_work':porcent_email_work, 'Q3':Q3,'Q4':Q4,'Q5':Q5,'Q6':Q6}
    return render(request, 'afficharge/bordeaux.html', context=context)

def paris(request):
    #Q1
    df_paris=pd.read_csv('/home/apprenant/Documents/Data/paris.csv')
    df_paris_reviews=pd.read_csv('/home/apprenant/Documents/Data/paris.csv')
    df_paris_neighbourhood=df_paris[["host_id","number_of_reviews","neighbourhood_cleansed"]].groupby("neighbourhood_cleansed").agg({"host_id":"count","number_of_reviews":"sum"})
    Q1=df_paris_neighbourhood.to_html(justify='left', classes='mystyle')
        

    #Q2
    df_verefication=df_paris[['host_verifications',"host_id"]]
    totale_verification=df_verefication.shape[0]
    number_phone=df_verefication[df_verefication['host_verifications'].str.contains('phone')]['host_verifications'].count()
    porcent_phone=(number_phone/totale_verification)*100
    number_email=df_verefication[df_verefication['host_verifications'].str.contains('email')]['host_verifications'].count()
    porcent_email=(number_email/totale_verification)*100
    number_email_work=df_verefication[df_verefication['host_verifications'].str.contains('work_email')]['host_verifications'].count()
    porcent_email_work=(number_email_work/totale_verification)*100


    #Q3

    df_room=df_paris[['room_type','amenities']]
    for i in range(df_room.shape[0]):
        A=df_room['amenities'][i]
        df_room['amenities'][i]=len(A.split(','))
    df_room['amenities']=df_room['amenities'].astype(float)
    df_room_mean=df_room.groupby('room_type').describe()
    #Q3=pd.DataFrame({'mean':df_room_mean.iloc[:,1],'std':df_room_mean.iloc[:,2]})
    Q3=df_room_mean.iloc[:,[1,2]].to_html(justify='left', classes='mystyle')
    
    #Q4
    df_price=df_paris[['room_type','price']]
    df_price['price']=df_price['price'].str.replace('$','')
    df_price['price']=df_price['price'].str.replace(',','')
    df_price['price']=df_price['price'].astype(float)
    df_price_describe=df_price.groupby('room_type').describe()
    Q4=df_price_describe.iloc[:,[3,4,6,7]].to_html(justify='left', classes='mystyle')
    #Q5 
    temp = (df_paris['bathrooms_text'].str.lower().str.contains('shared') * 0.5)+ (df_paris['bathrooms_text'].str.lower().str.contains('half') * 0.5)
    temp[temp == 1] = 0.25
    temp[temp == 0] = 1
    temp.fillna(1, inplace=True)
    df_paris['bathrooms_cleaned'] = df_paris.bathrooms_text.str.replace(r'[a-zA-Z]', '').str.replace('-', '').str.strip()
    df_paris[df_paris['bathrooms_cleaned'] == ''] = np.nan
    df_paris['bathrooms_cleaned'] = df_paris['bathrooms_cleaned'].astype('float')
    df_paris['bathrooms_cleaned'] = df_paris['bathrooms_cleaned'] * temp
    df_paris['bathrooms_cleaned'].unique()
    Q5=pd.DataFrame({'prix':df_paris['bathrooms_cleaned'].value_counts().sort_index()})
    Q5=Q5.to_html(justify='left', classes='mystyle')
    #Q6
    Q6=df_paris['description'].str.len().corr(df_paris['number_of_reviews'])
    #Q7
    # df_merged_reivews = df_paris[['id', 'host_name']].merge(df_paris_reviews[['listing_id', 'reviewer_name']],left_on='id',right_on='listing_id' )
    # Q7=(df_merged_reivews['host_name'] == df_merged_reivews['reviewer_name']).sum() / len(df_merged_reivews)

    context={'Q1':Q1,'porcent_phone':porcent_phone, 'porcent_email':porcent_email,'porcent_email_work':porcent_email_work, 'Q3':Q3,'Q4':Q4,'Q5':Q5,'Q6':Q6}
    return render(request, 'afficharge/paris.html', context=context)
def lyon(request):
    #Q1
    df_lyon=pd.read_csv('/home/apprenant/Documents/Data/lyon.csv')
    df_lyon_reviews=pd.read_csv('/home/apprenant/Documents/Data/lyon.csv')
    df_lyon_neighbourhood=df_lyon[["host_id","number_of_reviews","neighbourhood_cleansed"]].groupby("neighbourhood_cleansed").agg({"host_id":"count","number_of_reviews":"sum"})
    Q1=df_lyon_neighbourhood.to_html(justify='left', classes='mystyle')
        

    #Q2
    df_verefication=df_lyon[['host_verifications',"host_id"]]
    totale_verification=df_verefication.shape[0]
    number_phone=df_verefication[df_verefication['host_verifications'].str.contains('phone')]['host_verifications'].count()
    porcent_phone=(number_phone/totale_verification)*100
    number_email=df_verefication[df_verefication['host_verifications'].str.contains('email')]['host_verifications'].count()
    porcent_email=(number_email/totale_verification)*100
    number_email_work=df_verefication[df_verefication['host_verifications'].str.contains('work_email')]['host_verifications'].count()
    porcent_email_work=(number_email_work/totale_verification)*100


    #Q3

    df_room=df_lyon[['room_type','amenities']]
    for i in range(df_room.shape[0]):
        A=df_room['amenities'][i]
        df_room['amenities'][i]=len(A.split(','))
    df_room['amenities']=df_room['amenities'].astype(float)
    df_room_mean=df_room.groupby('room_type').describe()
    #Q3=pd.DataFrame({'mean':df_room_mean.iloc[:,1],'std':df_room_mean.iloc[:,2]})
    Q3=df_room_mean.iloc[:,[1,2]].to_html(justify='left', classes='mystyle')
    
    #Q4
    df_price=df_lyon[['room_type','price']]
    df_price['price']=df_price['price'].str.replace('$','')
    df_price['price']=df_price['price'].str.replace(',','')
    df_price['price']=df_price['price'].astype(float)
    df_price_describe=df_price.groupby('room_type').describe()
    Q4=df_price_describe.iloc[:,[3,4,6,7]].to_html(justify='left', classes='mystyle')
    #Q5 
    temp = (df_lyon['bathrooms_text'].str.lower().str.contains('shared') * 0.5)+ (df_lyon['bathrooms_text'].str.lower().str.contains('half') * 0.5)
    temp[temp == 1] = 0.25
    temp[temp == 0] = 1
    temp.fillna(1, inplace=True)
    df_lyon['bathrooms_cleaned'] = df_lyon.bathrooms_text.str.replace(r'[a-zA-Z]', '').str.replace('-', '').str.strip()
    df_lyon[df_lyon['bathrooms_cleaned'] == ''] = np.nan
    df_lyon['bathrooms_cleaned'] = df_lyon['bathrooms_cleaned'].astype('float')
    df_lyon['bathrooms_cleaned'] = df_lyon['bathrooms_cleaned'] * temp
    df_lyon['bathrooms_cleaned'].unique()
    Q5=pd.DataFrame({'prix':df_lyon['bathrooms_cleaned'].value_counts().sort_index()})
    Q5=Q5.to_html(justify='left', classes='mystyle')
    #Q6
    Q6=df_lyon['description'].str.len().corr(df_lyon['number_of_reviews'])
    #Q7
    # df_merged_reivews = df_lyon[['id', 'host_name']].merge(df_lyon_reviews[['listing_id', 'reviewer_name']],left_on='id',right_on='listing_id' )
    # Q7=(df_merged_reivews['host_name'] == df_merged_reivews['reviewer_name']).sum() / len(df_merged_reivews)

    context={'Q1':Q1,'porcent_phone':porcent_phone, 'porcent_email':porcent_email,'porcent_email_work':porcent_email_work, 'Q3':Q3,'Q4':Q4,'Q5':Q5,'Q6':Q6}
    return render(request, 'afficharge/lyon.html', context=context)

def basque(request):
    #Q1
    df_basque=pd.read_csv('/home/apprenant/Documents/Data/basque.csv')
    df_basque_reviews=pd.read_csv('/home/apprenant/Documents/Data/basque.csv')
    df_basque_neighbourhood=df_basque[["host_id","number_of_reviews","neighbourhood_cleansed"]].groupby("neighbourhood_cleansed").agg({"host_id":"count","number_of_reviews":"sum"})
    Q1=df_basque_neighbourhood.to_html(justify='left', classes='mystyle')
        

    #Q2
    df_verefication=df_basque[['host_verifications',"host_id"]]
    totale_verification=df_verefication.shape[0]
    number_phone=df_verefication[df_verefication['host_verifications'].str.contains('phone')]['host_verifications'].count()
    porcent_phone=(number_phone/totale_verification)*100
    number_email=df_verefication[df_verefication['host_verifications'].str.contains('email')]['host_verifications'].count()
    porcent_email=(number_email/totale_verification)*100
    number_email_work=df_verefication[df_verefication['host_verifications'].str.contains('work_email')]['host_verifications'].count()
    porcent_email_work=(number_email_work/totale_verification)*100


    #Q3

    df_room=df_basque[['room_type','amenities']]
    for i in range(df_room.shape[0]):
        A=df_room['amenities'][i]
        df_room['amenities'][i]=len(A.split(','))
    df_room['amenities']=df_room['amenities'].astype(float)
    df_room_mean=df_room.groupby('room_type').describe()
    #Q3=pd.DataFrame({'mean':df_room_mean.iloc[:,1],'std':df_room_mean.iloc[:,2]})
    Q3=df_room_mean.iloc[:,[1,2]].to_html(justify='left', classes='mystyle')
    
    #Q4
    df_price=df_basque[['room_type','price']]
    df_price['price']=df_price['price'].str.replace('$','')
    df_price['price']=df_price['price'].str.replace(',','')
    df_price['price']=df_price['price'].astype(float)
    df_price_describe=df_price.groupby('room_type').describe()
    Q4=df_price_describe.iloc[:,[3,4,6,7]].to_html(justify='left', classes='mystyle')
    #Q5 
    temp = (df_basque['bathrooms_text'].str.lower().str.contains('shared') * 0.5)+ (df_basque['bathrooms_text'].str.lower().str.contains('half') * 0.5)
    temp[temp == 1] = 0.25
    temp[temp == 0] = 1
    temp.fillna(1, inplace=True)
    df_basque['bathrooms_cleaned'] = df_basque.bathrooms_text.str.replace(r'[a-zA-Z]', '').str.replace('-', '').str.strip()
    df_basque[df_basque['bathrooms_cleaned'] == ''] = np.nan
    df_basque['bathrooms_cleaned'] = df_basque['bathrooms_cleaned'].astype('float')
    df_basque['bathrooms_cleaned'] = df_basque['bathrooms_cleaned'] * temp
    df_basque['bathrooms_cleaned'].unique()
    Q5=pd.DataFrame({'prix':df_basque['bathrooms_cleaned'].value_counts().sort_index()})
    Q5=Q5.to_html()
    #Q6
    Q6=df_basque['description'].str.len().corr(df_basque['number_of_reviews'])
    #Q7
    # df_merged_reivews = df_basque[['id', 'host_name']].merge(df_basque_reviews[['listing_id', 'reviewer_name']],left_on='id',right_on='listing_id' )
    # Q7=(df_merged_reivews['host_name'] == df_merged_reivews['reviewer_name']).sum() / len(df_merged_reivews)

    context={'Q1':Q1,'porcent_phone':porcent_phone, 'porcent_email':porcent_email,'porcent_email_work':porcent_email_work, 'Q3':Q3,'Q4':Q4,'Q5':Q5,'Q6':Q6}
    return render(request, 'afficharge/basque.html', context=context)

    
class UserCreateView(CreateView):
    form_class = forms.UserCreationFormCustom
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
