# Presentation – cirka fem minuter

Öva med appen öppen. Anpassa de markerade delarna till egna erfarenheter. Tiderna är ungefärliga och inkluderar klick och korta pauser.

## 0:00–0:40 – Område och syfte

”Mitt projekt handlar om interaktiv dataanalys med Streamlit och Pandas. Syftet är att göra det enkelt att ladda upp en CSV-fil och få en första förståelse av innehållet.

Jag valde området eftersom jag ville lära mig mer om hur man läser och visar CSV-data. Appen fokuserar på datans struktur, saknade värden och fördelningar. Den tränar inga modeller och använder ingen databas.”

## 0:40–1:25 – Viktiga begrepp

”En CSV-fil är en textfil där värden skiljs åt med exempelvis komma eller semikolon. Pandas läser filen till en DataFrame, som är en tabell med rader och kolumner.

Kolumnerna har datatyper. Det spelar roll eftersom vi behöver numeriska data för att exempelvis räkna medelvärden och rita histogram.

Streamlit skapar gränssnittet. Filuppladdaren och rullistorna är widgets. När användaren ändrar ett val körs skriptet om och resultatet uppdateras.”

## 1:25–1:55 – Vad lösningen innehåller

”Appen visar antalet rader och kolumner, en förhandsgranskning och en sammanställning av datatyper och saknade värden. Användaren kan välja kolumner och undersöka statistiken.

Det finns också ett histogram och ett lådagram. De fungerar för en enda numerisk kolumn, så en liten fil räcker för att använda båda diagrammen.”

## 1:55–3:15 – Demonstration

Ladda upp `sample_data.csv` med filväljaren. Ha kryssrutan för exempeldata avmarkerad. Om filväljaren strular kan exempeldata användas som reserv, men säg då vad du gör.

”Här använder jag påhittade produktdata. Filen innehåller tolv rader och fyra kolumner. Vi ser att kategori, pris och antal har ett saknat värde var. Appen fyller inte i något själv.”

Visa prisstatistiken och välj pris för diagrammen.

”Det finns elva ifyllda priser. Medianen är 79 och medelvärdet cirka 85,91. De högre priserna drar upp medelvärdet. Histogrammet visar hur värdena fördelas mellan intervall. Lådagrammet visar median och spridning. En punkt utanför spröten betyder inte automatiskt att värdet är fel.”

Byt diagramkolumn till antal. Välj sedan enbart produkt i kolumnvalet.

”När jag ändrar kolumn uppdateras diagrammen. Om jag väljer enbart text får jag information om att numeriska data saknas. Appen kraschar inte.”

## 3:15–4:15 – Förklara en funktion

Öppna `app.py` och visa `summarize_columns()`.

”Den här funktionen tar emot hela tabellen och skapar en ny sammanställning. `data.dtypes` hämtar datatyperna. `data.isna()` ger sant där ett värde saknas och falskt där det finns ett värde.

När vi använder `sum()` räknas sant som ett och falskt som noll. Resultatet blir antalet saknade värden per kolumn. `mean()` ger andelen, som multipliceras med hundra för att visas i procent. Resultatet avrundas till en decimal.

Funktionen ändrar inte den ursprungliga tabellen. Att lägga beräkningen i en separat funktion gör den enklare att läsa och testa.”

## 4:15–5:00 – Lärdomar och begränsningar

”Det viktigaste jag själv lärde mig var att Pandas läser och hanterar data medan Streamlit visar resultatet. Det jag behövde lägga mest tid på var att förstå statistikbegrepp och funktionernas uppgifter.

Appen är avsedd för mindre filer och kräver UTF-8. Automatisk typbestämning fungerar inte alltid som användaren tänkt. Därför är tabellen med datatyper viktig att granska.

Testerna kontrollerar databehandling och flera flöden i ett simulerat Streamlit-gränssnitt. Jag har laddat upp en CSV-fil med 2 000 rader och 17 kolumner och testat en tom fil som gav ett tydligt felmeddelande. Ett möjligt nästa steg är ett spridningsdiagram för att undersöka samband mellan två numeriska kolumner.”

## Fem möjliga lärarfrågor

1. **Varför använder du både Streamlit och Pandas?** Pandas läser och analyserar data. Streamlit visar resultat och tar emot användarens val. Biblioteken löser olika delar av uppgiften.
2. **Varför fyller du inte i saknade värden automatiskt?** Lämplig metod beror på vad datan betyder. Att fylla i noll eller medelvärde kan snedvrida analysen. Appen visar problemet så att användaren kan bedöma det.
3. **Vad händer om en kolumn innehåller både tal och text?** Pandas kan tolka hela kolumnen som text. Då erbjuds den inte som numerisk diagramkolumn. Användaren behöver kontrollera filens innehåll och format.
4. **Vad är skillnaden mellan median och medelvärde?** Medelvärdet är summan delad med antalet värden. Medianen är mittenvärdet i sorterad data, eller medelvärdet av de två mittersta. Medianen påverkas mindre av extremvärden.
5. **Hur vet du att felhanteringen fungerar?** Tester använder bland annat tomma filer och ojämna CSV-rader och kontrollerar felmeddelanden. AppTest testar flera gränssnittsflöden. Simulerad uppladdning verifierar inte den riktiga filväljaren; den behöver också provas manuellt.
