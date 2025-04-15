import re

def parsiraj_sms(poruka: str) -> dict:
    # Pokušaj da prepoznaš format poruke sa karticom
    match = re.search(r'POTROSNJA po kartici (\d{6})\*\*\d{4} Iznos ([\d\.,]+) (EUR|RSD) Datum (\d{2}\.\d{2}\.\d{4}) Trgovac (.+?) ', poruka)
    
    if match:
        # Ekstraktuj podatke
        kartica = match.group(1)
        iznos = float(match.group(2).replace(',', '.'))
        valuta = match.group(3)
        datum = match.group(4)
        trgovac = match.group(5)

        # Formatiraj datum u yyyy-mm-dd
        dan, mesec, godina = datum.split('.')
        datum_iso = f"{godina}-{mesec}-{dan}"

        # Ako je valute EUR, treba da obeležimo
        if valuta == "EUR":
            iznos = iznos  # Ostavljamo iznos u EUR
            kategorija = "Online kupovina"
        elif valuta == "RSD":
            iznos = iznos  # Ostaviti iznos u RSD
            kategorija = "Ostalo"
        else:
            kategorija = "Nepoznato"

        return {
            "datum": datum_iso,
            "vreme": "Ne dostupno",  # Možemo dodati ako bude potrebno
            "iznos": iznos,
            "prodavac": trgovac,
            "kategorija": kategorija
        }

    # U slučaju da nije odgovarajući format poruke, povratiti grešku
    raise ValueError("Poruka nije prepoznata ili je u nepoznatom formatu.")
