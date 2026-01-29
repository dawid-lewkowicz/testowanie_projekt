# behave tests/bdd/features/scenario.feature

Feature: Zakup samochodu

  Scenario: Udany zakup samochodu
    Given Mamy dostępne auto marki "Opel" o cenie 5000 i VIN "123ABC_CLEAN"
    And Mamy użytkownika "Kowalski" z portfelem 10000
    When Użytkownik kupuje to auto
    Then Auto zostaje oznaczone jako sprzedane
    And Stan konta użytkownika wynosi 5000

  Scenario: Zakup auta przy niewystarczających środkach
    Given Mamy dostępne auto marki "Ferrari" o cenie 500000 i VIN "123ABC_CLEAN"
    And Mamy użytkownika "Dawid" z portfelem 1000
    When Użytkownik kupuje to auto
    Then Operacja kończy się błędem "Niewystarczające środki na koncie"
    And Stan konta użytkownika wynosi 1000

  Scenario: Próba zakupu auta z wypadkową historią
    Given Mamy dostępne auto marki "BMW" o cenie 50000 i VIN "123ABC_X"
    And Mamy użytkownika "Dawid" z portfelem 100000
    When Użytkownik kupuje to auto
    Then Operacja kończy się błędem "Auto ma wypadkową historię"
    And Auto nie zostaje oznaczone jako sprzedane

  Scenario: Weryfikacja listy dostępnych samochodów
    Given Mamy dostępne auto marki "Toyota" o cenie 30000 i VIN "123ABC_CLEAN"
    And Mamy użytkownika "Dawid" z portfelem 0
    When Użytkownik sprawdza listę aut
    Then Na liście znajduje się auto marki "Toyota"