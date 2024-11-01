import requests
from datetime import datetime, time

BASE_URL = "http://127.0.0.1:8000"

def visa_lediga_rum_vecka():
    url = f"{BASE_URL}/available-rooms-week"
    response = requests.get(url)
    if response.status_code == 200:
        week_availability = response.json()
        for date, rooms in week_availability.items():
            day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%A")  # Konvertera datum till veckodag
            print(f"{day_name} ({date}):")
            for room, tider in rooms.items():
                print(f"  {room}: {', '.join(tider) if tider else 'Inga lediga tider'}")
            print()
    else:
        print("Kunde inte hämta lediga rum för veckan.")

# Uppdatera huvudmenyn för att visa veckans lediga rum
def boka_rum_terminal():
    print("Välkommen till bokningssystemet!")
    while True:
        try:
            visa_lediga_rum_vecka()  # Visa veckans lediga rum först
            room_choice = int(input("Välj ett rum att boka (1-5) eller 0 för att avsluta: "))
            if room_choice == 0:
                print("Avslutar bokningssystemet.")
                break
            elif room_choice not in range(1, 6):
                print("Ogiltigt val. Välj ett rumsnummer mellan 1 och 5.")
                continue

            datum = input("Ange ett datum att boka (YYYY-MM-DD): ")
            try:
                booking_date = datetime.strptime(datum, "%Y-%m-%d").date()
                today = datetime.today().date()
                if booking_date < today:
                    print("Datumet ligger i det förflutna. Välj ett framtida datum.")
                    continue
                if booking_date.weekday() > 4:
                    print("Endast bokningar mellan måndag och fredag är tillåtna.")
                    continue
            except ValueError:
                print("Felaktigt datumformat. Ange datumet i formatet YYYY-MM-DD.")
                continue

            tid = input("Ange en tid att boka (08:00 - 17:00) i format HH:MM: ")
            try:
                tid_obj = datetime.strptime(tid, "%H:%M").time()
                if not (time(8, 0) <= tid_obj <= time(17, 0)):
                    print("Ogiltig tid. Tiden måste vara mellan 08:00 och 17:00.")
                    continue
            except ValueError:
                print("Felaktigt tidsformat. Ange tiden i formatet HH:MM.")
                continue

            boka_rum_via_api(room_choice, tid, datum)

        except ValueError:
            print("Felaktig inmatning. Försök igen.")

# Uppdatera boka_rum_via_api för att inkludera datum
def boka_rum_via_api(room_id: int, tid: str, datum: str):
    url = f"{BASE_URL}/book-room"
    data = {"room_id": room_id, "tid": tid, "datum": datum}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(response.json()["detail"])

# Starta menyn
boka_rum_terminal()
