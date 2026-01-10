Feature: Zakup samochodu

  Scenario: Udany zakup samochodu
    Given Mamy dostępne auto marki "Opel" o cenie 5000 i VIN "123ABC_CLEAN"
    And Mamy użytkownika "Kowalski" z portfelem 10000
    When Użytkownik kupuje to auto
    Then Auto zostaje oznaczone jako sprzedane
    And Stan konta użytkownika wynosi 5000