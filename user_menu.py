import requests
from datetime import datetime, time

BASE_URL = "http://127.0.0.1:8000"

def visa_lediga_rum():
    url = f"{BASE_URL}/available-rooms"
    response = requests.get(url)
    if response.status_code == 200:
        available_rooms = response.json()
        if available_rooms:
            for room, tider in available_rooms.items():
                print(f"{room}: {', '.join(tider)}")
        else:
            print("Inga lediga rum finns för idag.")
    else:
        print("Kunde inte hämta lediga rum.")

# Funktion för att boka ett rum via API:t, skickar JSON-data
def boka_rum_via_api(room_id: int, tid: str, datum: str):
    url = f"{BASE_URL}/book-room"
    data = {"room_id": room_id, "tid": tid, "datum": datum}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(response.json()["detail"])

# Huvudmenyn för bokningssystemet
def boka_rum_terminal():
    print("Välkommen till bokningssystemet!")
    while True:
        try:
            visa_lediga_rum()
            room_choice = int(input("Välj ett rum att boka (1-5) eller 0 för att avsluta: "))
            if room_choice == 0:
                print("Avslutar bokningssystemet.")
                break
            elif room_choice not in range(1, 6):
                print("Ogiltigt val. Välj ett rumsnummer mellan 1 och 5.")
                continue

            datum = input("Ange ett datum att boka (YYYY-MM-DD): ")
            tid = input("Ange en tid att boka (08:00 - 17:00) i format HH:MM: ")
            
            boka_rum_via_api(room_choice, tid, datum)

        except ValueError:
            print("Felaktig inmatning. Försök igen.")

# Starta menyn
boka_rum_terminal()
