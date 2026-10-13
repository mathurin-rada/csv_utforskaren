# CSV-utforskaren

En liten interaktiv app för att undersöka CSV-data med Python, Streamlit och Pandas. Projektet fokuserar på grundläggande dataanalys: att förstå datans struktur, upptäcka saknade värden och undersöka fördelningar. Inga databaser, API-nycklar eller maskininlärningsmodeller används.

## Funktioner

- Uppladdning av CSV-filer eller val av medföljande exempeldata.
- Antal rader och kolumner, datatyper och saknade värden i antal och procent.
- Val av kolumner, förhandsgranskning av 20 rader och beskrivande statistik.
- Histogram och lådagram för en vald numerisk kolumn.
- Begripliga meddelanden för bland annat tomma filer, felaktiga rader och avsaknad av numeriska data.

## Installation och start

Använd Python 3.12 eller 3.13. Projektets virtuella miljö på den här datorn använder Python 3.13. Öppna en terminal i mappen som innehåller `app.py`.

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Kommandona använder miljön direkt, så något aktiveringsskript behövs inte. Om `py` saknas men `python` fungerar, använd `python -m venv .venv` i första steget. Kontrollera först versionen med `python --version`.

macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Öppna adressen som terminalen visar, normalt http://localhost:8501. Avsluta med Ctrl+C i terminalen.

## Använda CSV-filer

1. Klicka på filuppladdaren och välj en CSV-fil.
2. Välj avgränsare: komma, semikolon eller tabb. Välj även decimalpunkt eller decimalkomma.
3. Kontrollera antal kolumner och förhandsgranskningen. Fel avgränsare kan göra att allt läses som en kolumn.
4. Granska saknade värden och välj vilka kolumner som ska ingå i analysen.
5. Välj en numerisk kolumn för de två diagrammen.

Filen ska vara UTF-8, högst 10 MB och ha unika, ifyllda rubriker på första raden. Alla datarader ska ha samma antal fält. Ett saknat värde anges med ett tomt fält, till exempel `Penna,,10`. Text med avgränsare omges av citattecken. Använd semikolon som avgränsare för filer med decimalkomma, eller citera decimalvärdena korrekt.

Pandas tolkar automatiskt datatyper och vanliga markörer för saknade värden, exempelvis `NA`. Kontrollera därför resultatet. Uppladdad data behandlas i minnet av appen och skrivs inte till en egen datafil av projektkoden. Om appen senare driftas på en server överförs filen till den servern.

## Exempeldata och demonstration

`sample_data.csv` innehåller 12 påhittade produkter och fyra kolumner: produkt, kategori, pris och antal. Inga personuppgifter används. Kategori, pris och antal har vardera ett saknat värde. Pris har 11 observationer, median 79 och medelvärde cirka 85,91.

Markera **Använd exempeldata** för en snabb demonstration. Exempeldata har företräde framför en uppladdad fil och läses alltid med sina egna fasta formatinställningar. Avmarkera rutan för att undersöka en uppladdning.

## Teknik och struktur

| Fil | Innehåll |
| --- | --- |
| `app.py` | CSV-inläsning, sammanställning och Streamlit-gränssnitt |
| `requirements.txt` | Streamlit, Pandas och Plotly |
| `sample_data.csv` | Påhittad demonstrationsdata |
| `test_app.py` | Automatiska tester med unittest och Streamlit AppTest |
| `TEST_RESULTS.md` | Verifieringsresultat och återstående manuella kontroller |
| `report.md` | Ursprungligt rapportutkast med platshållare |
| `report_kompletterad.md` | Kompletterad rapport; granska namn och egna erfarenheter före inlämning |
| `presentation_notes_kompletterad.md` | Manus för cirka fem minuter och lärarfrågor |

`load_csv()` avkodar, kontrollerar CSV-strukturen och skapar en DataFrame. `summarize_columns()` räknar saknade värden och visar datatyper. `show_charts()` väljer numeriska data och bygger diagrammen. `main()` kopplar samman filval, tabeller och diagram. Streamlit kör om skriptet när ett val ändras.

## Tester

Från projektmappen, efter installation:

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

Se `TEST_RESULTS.md` för exakt vad som verifierats. Testerna använder AppTests simulerade filuppladdningswidget; de bevisar inte att webbläsarens filväljare fungerar.

## Begränsningar

Appen är gjord för mindre filer. Den läser hela filen i minnet vid varje omkörning. Förhandsgranskningen begränsas till 20 rader, medan statistiken använder alla rader. Datum omvandlas inte automatiskt till datumobjekt och text som ser ut som tal rättas inte manuellt. Appen fyller inte i saknade värden. Oändliga värden utelämnas ur diagrammen men kan påverka statistiken. Numeriska identifierare kan ge ointressanta diagram; användaren måste välja meningsfulla variabler. Ett diagram med en enda observation går att visa men ger mycket lite analysunderlag.

## Inför GitHub-inlämning

- [ ] Läs och förstå alla fyra funktionerna i `app.py`.
- [ ] Installera och starta appen på den dator som ska användas vid presentationen.
- [ ] Ladda upp `sample_data.csv` med filväljaren och följ manuella kontroller i `TEST_RESULTS.md`.
- [ ] Fyll i självreflektionen, personliga motiveringar och eventuella kursuppgifter i rapporten.
- [ ] Jämför projektet med lärarens fullständiga G-kriterier, som inte fanns i underlaget.
- [ ] Följ kursens regler för AI-stöd och beskriv det stöd du faktiskt har använt.
- [ ] Kontrollera att inga känsliga filer, virtuella miljöer eller hemligheter följer med.
- [ ] Lägg upp projektfilerna, inklusive `.gitignore`, i det avsedda GitHub-repot och kontrollera länken.
- [ ] Öva presentationen och prova att svara på frågorna utan att läsa innantill.

Projektet förbereds för publicering på GitHub med studentens godkännande.
