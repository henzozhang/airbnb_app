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
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from dotenv import load_dotenv 
load_dotenv()
import os 

def home_page(request):
    return render(request, 'afficharge/home_page.html')

def valeur_salle_de_bain(x):
    x_list = x.split(" ")
    x_value = 1
    mapper = {"bath":1, "baths":1, "private":2, "shared":0.5, "half-bath":0.5}
    for element in x_list:
        try: 
            x_value *= float(element)
        except:
            x_value *= mapper[element.lower()]
    return x_value

def function(listing, reviews, xsize=8, ysize=6 ):

    df_ville = pd.read_csv('/home/apprenant/Documents/Data/{}'.format(listing))

    #Q1
    df_ville_neighbourhood = df_ville[["host_id","number_of_reviews","neighbourhood_cleansed"]].groupby("neighbourhood_cleansed").agg({"host_id":"count","number_of_reviews":"sum"})
    Q1 = df_ville_neighbourhood.to_html(justify='left', classes='mystyle')

    # Affichage
    nombre_host = df_ville.groupby('neighbourhood_cleansed').host_id.nunique()
    nombre_review = df_ville.groupby('neighbourhood_cleansed').number_of_reviews.sum()
    neigbourhood = pd.concat([nombre_host,nombre_review], axis = 1)
    neigbourhood.columns = ["host_number", "review_number"]
    neigbourhood = neigbourhood.sort_values(by="host_number", ascending=True).tail(20)

    x = np.arange(neigbourhood.shape[0])  # the label locations
    width = 0.2

    plt.figure(figsize=(xsize, ysize))

    plt.bar(x - width , neigbourhood["host_number"], width, label="Nombre d'hôtes")
    plt.bar(x + width , neigbourhood["review_number"]/100 , width, label="Nombre de commentaires en centaines")


    plt.xticks(ticks=x, labels=neigbourhood.index)
    plt.tick_params(axis='x',labelrotation=90.0)

    plt.title("Nombre d'hôtes et de commentaires par quartier")
    plt.legend()
    plt.savefig('static/img/question1.png', bbox_inches='tight')

    #Q2
    response_rate = df_ville["host_response_rate"].dropna().apply(lambda x : x.replace("%","")).astype("int").mean()
    acceptance_rate = df_ville["host_acceptance_rate"].dropna().apply(lambda x : x.replace("%","")).astype("int").mean()

    plt.figure(figsize=(xsize,ysize))

    # On indique ensuite que notre figure comportera une ligne, deux colonnes, et qu'on travaille sur le premier graphe
    plt.subplot(1,2,1)

    # On crée ensuite notre figure
    plt.pie(x=[response_rate,100-response_rate], labels=["Oui","Non"])

    # on ajoute les titres
    plt.title("A répondu à une demande de séjour")
    # On ajoute pas de légende car c'est compliqué avec matplot. On utilisera pour ça d'autres librairies

    # On travaille maintenant sur le second graphe
    plt.subplot(1,2,2)

    # On crée ensuite notre figure

    # On crée ensuite notre figure
    plt.pie(x=[acceptance_rate,100-response_rate], labels=["Oui","Non"],  autopct='%.2f')

    # on ajoute les titres
    plt.title("A accepté à une demande de séjour")
    plt.savefig('static/img/question2.png', bbox_inches='tight')

    #Q3
    df_verefication = df_ville[['host_verifications',"host_id"]]
    totale_verification = df_verefication.shape[0]

    number_phone = df_verefication[df_verefication['host_verifications'].str.contains('phone')]['host_verifications'].count()
    porcent_phone = round((number_phone/totale_verification)*100, 2)

    number_email = df_verefication[df_verefication['host_verifications'].str.contains('email')]['host_verifications'].count()
    porcent_email = round((number_email/totale_verification)*100)

    number_email_work = df_verefication[df_verefication['host_verifications'].str.contains('work_email')]['host_verifications'].count()
    porcent_email_work = round((number_email_work/totale_verification)*100)

    #Affichage
    plt.figure()

    plt.bar(['téléphone', 'email', 'email professionnel'], [porcent_phone, porcent_email, porcent_email_work], color='green')

    plt.title("Taux de vérification par canal")
    plt.ylabel("Taux de vérification en pourcentage")
    plt.xlabel("Canal de vérification")
    plt.savefig('static/img/question3.png', bbox_inches='tight')

    #Q4
    df_ville["nb_amenities"] = df_ville["amenities"].apply(eval).apply(len)
    df_amenities = np.round(df_ville[["nb_amenities","room_type"]].groupby("room_type").agg(["mean","std"]), 2)
    df_amenities.columns = ["mean_am","std_am"]
    Q4 = df_amenities.to_html(justify='left', classes='mystyle')
    
    #Affichage
    plt.figure()

    plt.bar(df_amenities.index,df_amenities["mean_am"])
    plt.errorbar(df_amenities.index,df_amenities["mean_am"], df_amenities["std_am"], fmt = 'none', 
                capsize = 10, ecolor = 'red', elinewidth = 1, capthick = 1)
    plt.title("Nombre de services par type de logement")
    plt.ylabel("Nombre de services disponibles")
    plt.xlabel("Types de logement")
    plt.savefig('static/img/question4.png', bbox_inches='tight')
    
    #Q5 
    df_ville["clean_price"] = df_ville["price"].apply(lambda x: x.replace("$","")).apply(lambda x: x.replace(",","")).astype("float")
    df_median = df_ville[["clean_price","room_type"]].groupby("room_type").agg(
    median_price = ('clean_price', 'median'), 
    max_price = ('clean_price', 'max'),
    min_price = ('clean_price', 'min'),
    first_quartile_price = ('clean_price',lambda x:x.quantile(0.25)),
    third_quartile_price = ('clean_price', lambda x:x.quantile(0.75)),
    )
    Q5 = df_median.to_html(justify='left', classes='mystyle')
 
    #Affichage
    plt.figure(figsize=(12,7))
    sns.boxplot(data = df_ville,x = "clean_price" ,y= "room_type", showfliers = False)
    plt.title("Distribution du prix des annonces par type de logement (sans les valeurs extrêmes")
    plt.savefig('static/img/question5.png', bbox_inches='tight')

    #Q6
    df_bath = df_ville["bathrooms_text"].dropna().apply(valeur_salle_de_bain)
    plt.figure(figsize=(10,6))

    g = sns.histplot(data=df_bath,bins=30)
    g.set_title("Distribution de la valeur de salles de bain")
    g.set_xlabel("Valeur de la salle de bain")
    g.set_ylabel("Nombre d'annonces correspondante")
    plt.savefig('static/img/question6.png', bbox_inches='tight')

    
    #Q7
    df_cor = df_ville[["description", "number_of_reviews"]].dropna()
    df_cor["description_len"] = df_cor["description"].apply(len) 
    df_cor[["description_len", "number_of_reviews"]].corr().to_html(justify='left', classes='mystyle')
    df_cor_sample = df_cor.sample(n=1000)

    #Affichage
    plt.figure(figsize=(8, 6))

    plt.scatter(df_cor_sample.description_len, df_cor_sample.number_of_reviews, s=2)
    plt.title("Nombre de commentaire en fonction de la taille de la description ")
    plt.xlabel("Nombre de caractère de la description")
    plt.ylabel(" Nombre de commentaires, par centaines")
    plt.savefig('static/img/question7.png', bbox_inches='tight')

    #Q8
    df_reviews = pd.read_csv('/home/apprenant/Documents/Data/{}'.format(reviews))
    df_merge = df_reviews.merge(df_ville, how="left", left_on="listing_id", right_on="id")
    df_name_idem = df_merge.loc[ df_merge["host_name"] == df_merge["reviewer_name"], ["host_name","reviewer_name"]]
    resultat = round(df_name_idem.shape[0]/df_merge.shape[0]*100, 5)

    #Affichage
    plt.figure()

    plt.pie(x=[resultat,100-resultat], labels=["Même nom",""], autopct='%1.0f%%')
    plt.legend()
    plt.savefig('static/img/question8.png', bbox_inches='tight')

    context = {'Q1':Q1,'porcent_phone':porcent_phone, 'porcent_email':porcent_email,'porcent_email_work':porcent_email_work,'Q4':Q4,'Q5':Q5}

    return context

def bordeaux(request):
    listing='bordeaux.csv'
    reviews = 'reviews_bordeaux.csv'
    context = function(listing, reviews, 15, 7)

    return render(request, 'afficharge/result.html', context=context)

def lyon(request):
    listing='lyon.csv'
    reviews = 'reviews_lyon.csv'
    context = function(listing, reviews)

    return render(request, 'afficharge/result.html', context=context)

def paris(request):
    listing='paris.csv'
    reviews = 'reviews_paris.csv'
    context = function(listing, reviews)

    return render(request, 'afficharge/result.html', context=context)

def basque(request):
    listing='basque.csv'
    reviews = 'reviews_basque.csv'
    context = function(listing, reviews, 15, 7)

    return render(request, 'afficharge/result.html', context=context)
   


class UserCreateView(CreateView):
    form_class = forms.UserCreationFormCustom
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'