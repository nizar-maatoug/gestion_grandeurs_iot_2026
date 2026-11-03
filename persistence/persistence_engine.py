from django.utils.dateparse import parse_datetime

from asgiref.sync import sync_to_async
import json
from django.apps import apps

import pyrebase
import firebase_admin
from firebase_admin import credentials

firebase_config = {
    "apiKey": "AIzaSyAOhDGvMEiidRc_uObr3Ul0Vb5aU1A2BSA",
    "authDomain": "flutterfirebaseapp-e151d.firebaseapp.com",
    "databaseURL": "https://gestion-grandeurs-2026-default-rtdb.europe-west1.firebasedatabase.app/",
    "projectId": "flutterfirebaseapp-e151d",
    "storageBucket": "flutterfirebaseapp-e151d.firebasestorage.app",
    "messagingSenderId": "173148386558",
    "appId": "1:173148386558:web:b646c093f09098fd1621af",
}

firebase=pyrebase.initialize_app(firebase_config)
database=firebase.database()

cred = credentials.Certificate("certificat_firebase.json")
firebase_admin.initialize_app(cred)



@sync_to_async
def persist_to_firebase(message):
    message = json.loads(message)
    print(f"Persisting to firebase: {message}")
    try:
        database.child("mesures").push(message)
    except Exception as e:
        print(f"Error occurred while persisting to firebase: {e}")

@sync_to_async
def persist_mesure(message):
    #from grandeurs.models import Grandeur, Mesure
    Grandeur = apps.get_model("grandeurs", "Grandeur")
    Mesure = apps.get_model("grandeurs", "Mesure")

    message = json.loads(message)

    grandeur = Grandeur.objects.get(nom="Temperature")
    print(f"Persisting mesure: {message}")
    Mesure.objects.create(
        valeur = float(message["valeur"]),
        date_prise = parse_datetime(message["date_prise"]),
        grandeur = grandeur
    )

buffer = []

@sync_to_async
def persist_mesure_bulk(message):
    from grandeurs.models import Grandeur, Mesure

    message = json.loads(message)

    global buffer

    buffer.append(
        Mesure(
            valeur = float(message["valeur"]),
            date_prise = parse_datetime(message["date_prise"])
        )
    )

    if len(buffer) >= 100:
        Mesure.objects.bulk_create(buffer)
        print(f"Inserted {len(buffer)} rows")
        buffer.clear()

