from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app=FastAPI()

class Utilisateur(BaseModel):
    nom: str
    numero: str
    mot_de_passe: str
class Conducteur(BaseModel):
    nom:str
    numero:str
    mot_de_passe:str 
class Numero_telephone(BaseModel):
    numero:str
connecter=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gestion_dechets_conducteur"
)
class connexion(BaseModel):
    numero:str
    mot_de_passe:str

@app.post("/verifier_utilisateur")
def verfier_utilisateur(numero_telephone:Numero_telephone):
    sql="SELECT * FROM utilisateur where numero=%s;"
    conn=connecter.cursor()
    conn.execute(sql,(numero_telephone.numero,))
    resultat=conn.fetchall()
    if resultat==[]:
        return{"existe":"false"}
    else:
        return {"existe":"true"}
@app.post("/ajouter_utilisateur")
def ajouter_utilisateur(utilisateur:Utilisateur):
    sql="INSERT INTO utilisateur (nom,numero,mot_de_passe) VALUES(%s,%s,%s);"
    conn=connecter.cursor()
    conn.execute(sql,(utilisateur.nom,utilisateur.numero,utilisateur.mot_de_passe))
    connecter.commit()
    return {"statut":"utilisateur ajouté"}
@app.get("/verifier_donnee")
def verifier_donnee():
    sql="SELECT * FROM utilisateur where  numero='0150161468' AND mot_de_passe='fresco2.0';"
    conn=connecter.cursor()
    conn.execute(sql)
    resultat=conn.fetchall()
    if resultat==[]:
        return{"existe":"false"}
    else:
        return {"existe":"true","resultat":resultat}