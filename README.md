Dawid Lewkowicz

Nr indeksu: 301575

Grupa: 3

Stworzyłem backend symulujący działanie komisu samochodowego.

Krótki opis:

- Handel autami: Można dodawać samochody do bazy i je kupować.
- Logika biznesowa: System pilnuje zasad – nie kupisz auta, jak masz za mało środków w portfelu albo jak auto jest już sprzedane.
- Weryfikacja VIN: Dodałem symulację zewnętrznego serwisu, który sprawdza historię pojazdu. Jak auto jest "powypadkowe" (VIN kończący się na "X") system blokuje transakcję.

Testy:

- Unit Testy: Sprawdzają, czy funkcje (walidacja ceny, dodawanie do bazy itd.) działają poprawnie w izolacji.
- Testy API: Strzelają do endpointów i sprawdzają, czy serwer zwraca dobre kody błędów i dane.
- BDD (Behave): Scenariusze pisane "ludzkim językiem" (Gherkin)
- Performance (Locust): Sprawdzenie, czy aplikacja wytrzyma, jak 10 użytkowników naraz zacznie kupować auta.

Uruchomienie testów:

- Unit Testy:
  pytest tests/unit
- Testy API:
  pytest tests/api
- DBB:
  behave tests/bdd/features/
- Performance:

  W jednym terminalu:
  python3 -m app.main

  W drugim terminalu
  locust -f tests/performance/locustfile.py

  Wchodzimy na http://localhost:8089

  Wpisujemy wartości i ustawiamy Hosta na: http://127.0.0.1:5000

- Pipeline CI/CD:
  Wyniki testów są widoczne w zakładce "Actions", testy te uruchamiają się samoczynnie przy pushowaniu kodu
