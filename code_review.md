# Code review – CSV-utforskaren

## Syfte
Jag har granskat projektets kod med fokus på tydlighet, felhantering, datakvalitet och testbarhet. Projektet har fyra huvudfunktioner i `app.py`: `load_csv()`, `summarize_columns()`, `show_charts()` och `main()`.

## Granskning och förbättringar

| Område | Risk eller problem | Lösning i den aktuella koden |
| --- | --- | --- |
| Filinläsning | En tom eller för stor fil kan ge problem. | `load_csv()` kontrollerar tomma filer och maxstorlek 10 MB och visar begripliga felmeddelanden. |
| CSV-format | Felaktiga rubriker eller olika antal fält kan ge missvisande data. | `csv.reader` kontrollerar rubriker och antal fält innan Pandas läser filen. |
| Saknade värden | Användaren kan missa att värden saknas. | `summarize_columns()` visar datatyp, antal saknade värden och procent för varje kolumn. |
| Diagram | Saknade eller oändliga värden kan göra diagram svåra att tolka. | `show_charts()` utesluter dessa värden från diagramdata utan att ändra originaltabellen. |
| Kodstruktur | All logik i en enda stor koddel blir svår att förstå och testa. | Koden är uppdelad i separata funktioner med tydliga uppgifter. |
| Tester | Fel kan vara svåra att upptäcka manuellt. | `test_app.py` testar datahantering, felaktiga filer och flera Streamlit-flöden. |

## Ett konkret fel som upptäcktes under testning
Enligt `TEST_RESULTS.md` hade ett test först fel förväntat medelvärde. De elva priserna hade summan 945, så korrekt medelvärde är 945 / 11 ≈ 85,91. Testets förväntade värde och dokumentationen rättades. Själva appens beräkning var korrekt.

## Resultat av tester
I `TEST_RESULTS.md` finns en tidigare körning dokumenterad: 13 automatiska tester, alla godkända. Jag har även manuellt provat att ladda upp en CSV-fil med 2 000 rader och 17 kolumner samt en tom CSV-fil. Den tomma filen gav ett tydligt felmeddelande.

## Begränsningar och möjliga förbättringar
Appen är gjord för mindre UTF-8-filer upp till 10 MB. Den gör ingen automatisk datarensning, och diagrammen använder en numerisk kolumn åt gången. En möjlig framtida förbättring är ett spridningsdiagram som visar samband mellan två numeriska kolumner.

## Reflektion
Kodgranskningen visar varför det är viktigt att kontrollera både beräkningar och felmeddelanden. Separata funktioner gör det lättare att förstå och testa projektet. AI-stöd användes vid framtagningen av lösningen och dokumentationen; jag har gått igenom funktionerna och testat appen manuellt.

> Obs: Detta dokument beskriver den nuvarande koden och den dokumenterade testhistoriken. Det påstår inte att alla förbättringar gjordes i en separat manuell refaktorering.
