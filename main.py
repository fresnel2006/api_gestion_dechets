from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app=FastAPI()

#class utilisateur
class Utilisateur(BaseModel):
    nom: str
    numero: str
    mot_de_passe: str

#class conducteur
class Conducteur(BaseModel):
    nom:str
    numero:str
    mot_de_passe:str 

#verifier cnducteur
class Verifier_conducteur(BaseModel):
    numero:str
    mot_de_passe:str

#class pour verifier si le numero des utilisateurs existe
class Numero_telephone(BaseModel):
    numero:str

#infomation de connexion a la base de donnee
connecter=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gestion_dechets_conducteur"
)
#class de connexion a un compte existant
class Connexion(BaseModel):
    numero:str
    mot_de_passe:str

#pour affiche les donnees des uilisateurs
class Donnee_utilisateur(BaseModel):
    numero:str

#pour envoyer les rapports des conducteurs
class Rapport(BaseModel):
    latitude:str
    longitude:str
    descriptions:str
    photo:str

#prendre trajet
class Trajet(BaseModel):
    id_trajet:str

#ajouter un rapport utilisateur
class Rapport_utilisateur(BaseModel):
    numero:str
    latitude:str
    longitude:str
    descriptions:str
    photo:str
    
#modifier information utilisateur
class Modification(BaseModel):
    nom: str
    numero: str
    mot_de_passe: str
    id_utilisateur: int

#verifier un utilisateur
@app.post("/verifier_utilisateur")
def verfier_utilisateur(numero_telephone:Numero_telephone):
    sql="SELECT * FROM utilisateur WHERE numero=%s;"
    conn=connecter.cursor()
    conn.execute(sql,(numero_telephone.numero,))
    resultat=conn.fetchall()
    if resultat==[]:
        return{"existe":"false"}
    else:
        return {"existe":"true","resultat":resultat}
    

#verifier un conducteur
@app.post("/verifier_conducteur")
def verifier_conducteur(verif_conducteur:Verifier_conducteur):
    sql="SELECT * FROM conducteur WHERE numero=%s AND mot_de_passe=%s;"
    conn=connecter.cursor()
    conn.execute(sql,(verif_conducteur.numero,verif_conducteur.mot_de_passe))
    resultat=conn.fetchall()
    if resultat==[]:
        return{"statut":"echec"}
    else:
        return {"statut":"succes","resultat":resultat}
    

#ajouter un utilisateur dans la base de donnee
@app.post("/ajouter_utilisateur")
def ajouter_utilisateur(utilisateur:Utilisateur):
    sql="INSERT INTO utilisateur (nom,numero,mot_de_passe) VALUES(%s,%s,%s);"
    conn=connecter.cursor()
    conn.execute(sql,(utilisateur.nom,utilisateur.numero,utilisateur.mot_de_passe))
    connecter.commit()
    return {"utilisateur":"utilisateur ajouté"}


#verifier les donnees d'un utilisateur
@app.post("/verifier_donnee")
def verifier_donnee(connexion:Connexion):
    sql="SELECT * FROM utilisateur WHERE numero=%s AND mot_de_passe=%s;"
    conn=connecter.cursor()
    conn.execute(sql,(connexion.numero,connexion.mot_de_passe))
    resultat=conn.fetchall()
    if resultat==[]:
        return{"existe":"false"}
    else:
        return {"existe":"true","resultat":resultat}
    
#afficher les donnees d'un utilisateur
@app.post("/afficher_donnee_utilisateur")
def afficher_donnee_utilisateur(donnee_utilisateur:Donnee_utilisateur):
    conn=connecter.cursor()
    sql="SELECT * FROM utilisateur WHERE numero=%s;"
    conn.execute(sql,(donnee_utilisateur.numero,))
    resultat=conn.fetchall()
    return {"resultat":resultat}

#ajouter un rapport dans la base de donnee
@app.post("/ajouter_rapport")
def ajouter_rapport(rapport:Rapport):
    sql="INSERT INTO rapports (latitude,longitude,descriptions,photo) VALUES(%s,%s,%s,%s);"
    conn=connecter.cursor()
    conn.execute(sql,(rapport.latitude,rapport.longitude,rapport.descriptions,rapport.photo))
    connecter.commit()
    return {"rapport":"rapport ajouté"}

#prendre un trajet
@app.post("/prendre_trajet")
def prendre_trajet(trajet:Trajet):
    sql="SELECT * FROM trajet WHERE id_trajet=%s;"
    conn=connecter.cursor()
    conn.execute(sql,(trajet.id_trajet,))
    resultat=conn.fetchall()
    return {"resultat":resultat}

@app.post("/envoyer_rapport_utilisateur")
def envoyer_rapport_utilisateur(rapport_utilisateur:Rapport_utilisateur):
    sql="INSERT INTO rapport (numero,latitude,longitude,descriptions,photo) VALUES(%s,%s,%s,%s,%s);"
    conn=connecter.cursor()
    conn.execute(sql,(rapport_utilisateur.numero,rapport_utilisateur.latitude,rapport_utilisateur.longitude,rapport_utilisateur.descriptions,rapport_utilisateur.photo))
    connecter.commit()
    return {"rapport_utilisateur":"rapport utilisateur ajouté"}

@app.get("/afficher_rapport")
def afficher_rapport():
    sql="SELECT * FROM rapport;"
    conn=connecter.cursor()
    conn.execute(sql)
    resultat=conn.fetchall()
    return {"resultat":resultat}

@app.post("/modifier_information")
def modifier_information(modification:Modification):
    sql="UPDATE utilisateur SET nom=%s,numero=%s ,mot_de_passe=%s WHERE id_utilisateur=%s;"
    conn=connecter.cursor()
    conn.execute(sql,(modification.nom,modification.numero,modification.mot_de_passe,modification.id_utilisateur))
    connecter.commit()
    return {"modification":"information modifiée"}