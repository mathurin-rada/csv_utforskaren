# Verifiering och kravkontroll

Datum: 12 oktober 2026. Kontrollerna nedan utfördes i Windows med Python 3.12.14, Streamlit 1.65.0, Pandas 3.0.6 och Plotly 6.9.0. Huvudbibliotekens versioner är låsta i `requirements.txt`; transitiva beroenden är inte fullständigt låsta.

## Utförda tester

Kommandot `python -m unittest -v` kördes från projektmappen med den separata testmiljöns Python. Slutresultat:

```text
Ran 13 tests in 1.645s
OK
```

Vid den förnyade granskningen återanvändes den befintliga lösningen utan nya appfunktioner. Alla 13 tester kördes om och passerade. Även serverstarten och HTTP-kontrollerna kördes om med godkänt resultat. Omfattningen är fortsatt enkel dataanalys med G som mål.

Fem testmetoder kontrollerar datalogiken: exempeldata och förväntad statistik, semikolon/decimalkomma/UTF-8-BOM, citerade fält och saknade värden, ogiltiga filer samt storleksgränsen. Testet för ogiltiga filer omfattar tio olika indatafall.

Åtta testmetoder använder Streamlit AppTest: start utan fil, uppladdning och förhandsgranskning, exempeldata och kolumnval, formatinställningar och byte/borttagning av fil, enbart text, helt saknad numerisk kolumn, ett enda numeriskt värde och användarsynliga felmeddelanden. Uppladdning görs genom AppTests filuppladdningswidget. Den slutliga testsviten ersätter inte `st.file_uploader` med en mock.

De två Plotly-elementen skapas i de testade numeriska fallen. Detta kontrollerar att appen producerar diagramobjekten; rendering, hovring och utseende i en faktisk webbläsare har inte verifierats. AppTest skriver varningar om saknad ScriptRunContext på huvudtråden. Testerna slutfördes utan appundantag i de verifierade flödena.

En separat process startades med `python -m streamlit run app.py --server.headless=true --server.address=127.0.0.1 --server.port=8517 --browser.gatherUsageStats=false`. Serverns hälsoadress `/_stcore/health` svarade HTTP 200 med `ok`, och startsidan svarade HTTP 200 med HTML. Processen stoppades efter kontrollen. Det bekräftar serverstart och HTTP-svar, men ersätter inte en webbläsardemonstration.

Under första testkörningen upptäcktes ett felaktigt förväntat medelvärde i testet. Summan av de elva priserna är 945 och medelvärdet är 945/11 ≈ 85,91. Förväntningen och motsvarande dokumentation rättades. Appens beräkning var korrekt.

## Kontroll mot samtliga funktionskrav i underlaget

| Krav | Implementation och verifiering |
| --- | --- |
| Ladda upp med `st.file_uploader` | Implementerat; widgetflödet testat i AppTest. Verklig filväljare återstår. |
| Läsa med Pandas | `load_csv()` använder `pd.read_csv()`; testat. |
| Förhandsgranskning | `head(20)` för valda kolumner; exempeldata och kolumnurval testade. |
| Antal rader och kolumner | `metric()` visar 12 och 4 för exempeldata; testat. |
| Kolumnnamn och datatyper | `summarize_columns()`; numerisk prisdatatyp och tabellens innehåll kontrollerade. |
| Identifiera och visa saknade värden | `isna().sum()` och procentandel; de kända saknade värdena testade. |
| Beskrivande statistik | `describe(include="all")`; antal, median och medelpris testade, textfall körda. |
| Välja kolumner | `multiselect()` och `selectbox()`; val, tomt urval och filbyte testade. |
| Minst två relevanta visualiseringar | Histogram och lådagram för vald numerisk kolumn; två diagramobjekt verifierade. Visuell kontroll återstår. |
| Tomma och felaktiga filer | UTF-8, rubriker, radlängder, citattecken och tom data kontrolleras; negativa testfall passerar. |
| Dataset utan numeriska kolumner | Meddelande i stället för diagram; testat. |
| Enkel och strukturerad kod | Fyra funktioner med avgränsade uppgifter; ingen databas eller maskininlärning. |
| README på svenska | Beskrivning, funktioner, teknik, installation, start, CSV-format, exempel och begränsningar finns. |
| Rapport på svenska | Alla tio begärda delar finns; personliga uppgifter och självreflektion återstår. |
| Muntlig presentation | Manus med tidsindelning för cirka fem minuter och fem frågor med svar finns. Egen övning återstår. |
| Säkra exempeldata och inga nycklar | Påhittade produkter; inga API-nycklar eller personuppgifter används. |
| Inga Git-commits/push utan godkännande | Inga Git-commits eller push har gjorts. |

## Bedömning av G-målet

De tekniska funktionerna i den tillgängliga beställningen är implementerade och kontrollerade enligt tabellen. Detta är inte ett formellt besked om G. Lärarens fullständiga betygsmatris finns inte i underlaget. Studenten behöver komplettera egna reflektioner, visa sin förståelse och jämföra materialet med de faktiska G-kriterierna. Inga VG-kriterier har antagits.

## Återstående manuella kontroller

- [ ] Installera enligt README på presentationsdatorn och öppna appen i en webbläsare.
- [ ] Använd den riktiga filväljaren för `sample_data.csv`, med exempelrutan avmarkerad. Kontrollera 12 rader och 4 kolumner.
- [ ] Kontrollera att å, ä och ö visas korrekt i exempelvis Skål och Pärm.
- [ ] Kontrollera att histogrammet och lådagrammet är synliga och läsbara. Byt från pris till antal och prova hovring.
- [ ] Välj bara produkt och kontrollera meddelandet om att numeriska data saknas. Töm sedan hela kolumnvalet.
- [ ] Ladda upp en tom fil och en fil med ojämna rader. Kontrollera begripliga felmeddelanden.
- [ ] Prova en egen liten CSV med semikolon och decimalkomma. Kontrollera att tal tolkas som tal.
- [ ] Öva demonstrationen och komplettera rapporten med vad du själv faktiskt observerat.

Inga manuella rutor är förkryssade eftersom de inte har genomförts i webbläsare under leveransen.
