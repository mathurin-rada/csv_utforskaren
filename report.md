# Interaktiv dataanalys med Streamlit och Pandas

**Namn:** Mathurin Radabud  
**Kurs:** Python Fördjupning (Data Science)  

Detta är ett rapportutkast utifrån den byggda lösningen. Personliga erfarenheter och den slutliga bedömningen ska fyllas i av studenten. Den fullständiga uppgiftsbeskrivningen med formella betygskriterier har inte varit tillgänglig.

## 1. Introduktion och fördjupningsområde

Projektets fördjupningsområde är interaktiv dataanalys i Python. Pandas används för att läsa och sammanställa data. Streamlit används för att göra analysen tillgänglig i en webbsida där användaren själv kan välja fil och kolumner. Plotly används för två typer av diagram.

**Min motivering till valet:** [Beskriv varför du valde området och vad du ville förstå bättre.]

## 2. Syfte och avgränsning

Syftet är att bygga en mindre applikation som hjälper användaren att få en första förståelse av en CSV-fil. Appen ska visa struktur, datakvalitet, grundläggande statistik och numeriska fördelningar. Den ska också reagera begripligt när en fil inte går att använda.

Projektet omfattar inte databaser, maskininlärning, inloggning eller automatisk datarensning. Avgränsningen gör det möjligt att fokusera på ett tydligt analysflöde och kod som går att förklara. Filerna begränsas till UTF-8 och högst 10 MB.

## 3. Relevans för Python och Data Science

En analys börjar ofta med att undersöka vad ett dataset innehåller. Antalet observationer, datatyper och saknade värden påverkar vilka analyser som är rimliga. En felaktigt tolkad sifferkolumn kan exempelvis hindra beräkningen av medelvärden.

Projektet kopplar ihop vanliga Python-delar som funktioner, villkor och undantag med Pandas tabellhantering. Streamlit gör analysen möjlig att prova utan att användaren själv skriver Python-kod. Diagrammen kompletterar statistiken genom att synliggöra spridning och möjliga avvikare.

## 4. Teoretisk bakgrund

En **CSV-fil** är text där avgränsare skiljer fälten åt. Komma och semikolon är vanliga avgränsare. Citattecken behövs när själva textvärdet innehåller en avgränsare. UTF-8 anger hur textens tecken representeras som byte.

En **DataFrame** är Pandas tabellstruktur med rader och namngivna kolumner. En kolumn har en datatyp som påverkar hur den kan behandlas. `read_csv()` kan dra slutsatser om datatyper och känna igen vanliga markörer för saknade värden. Den tolkningen behöver kontrolleras av användaren.

**Saknade värden** är observationer där information inte finns registrerad. `isna()` skapar en tabell av booleska värden. När dessa summeras per kolumn räknas antalet saknade värden. Andelen beräknas med medelvärdet av samma booleska värden, multiplicerat med 100.

**Beskrivande statistik** sammanfattar data. Medelvärdet använder alla tillgängliga numeriska värden, medan medianen är värdet i mitten av den sorterade fördelningen. Standardavvikelsen beskriver spridningen. Pandas `describe()` visar även kvartiler. För textkolumner kan metoden visa antal unika värden och det vanligaste värdet. Saknade värden räknas inte in i `count`.

Ett **histogram** grupperar numeriska värden i intervall och visar frekvenser. Ett **lådagram** visar median och kvartiler. Lådan går från första till tredje kvartilen. Spröten sträcker sig till observationer inom 1,5 kvartilavstånd från lådan enligt diagrammets standardregel. Punkter utanför kan vara avvikare men behöver inte vara fel. Dessa diagram fungerar även när datasetet bara har en numerisk kolumn.

En **Streamlit-widget** är exempelvis en filuppladdare eller en rullista. När användaren ändrar ett val kör Streamlit normalt om skriptet och bygger om resultatet utifrån de aktuella valen.

## 5. Genomförande och projektstruktur

Arbetsmappen undersöktes först. Den innehöll ingen befintlig projektkod. Därefter skapades `app.py`, beroendelistan, exempeldata, tester och dokumentation. Projektet använder ett litet antal funktioner i samma appfil för att hålla strukturen lätt att följa.

Flödet är: fil eller exempeldata → formatkontroll → DataFrame → översikt → kolumnval → statistik och diagram. Filuppladdningen görs med `st.file_uploader`. Användaren kan ange avgränsare och decimaltecken. Exempeldata kan också väljas utan uppladdning.

`README.md` beskriver installation och användning. `test_app.py` innehåller automatiska tester. `TEST_RESULTS.md` skiljer utförda kontroller från sådant som återstår. `presentation_notes.md` stödjer den muntliga demonstrationen.

**AI-stöd och eget arbete:** Lösningen och dokumentationsutkastet har tagits fram med AI-stöd. [Komplettera med hur du granskade, ändrade, testade och förstod materialet. Anpassa redovisningen till kursens regler.]

## 6. Viktiga delar av koden

### Inläsning och felhantering

`load_csv()` tar emot filens byte samt avgränsare och decimaltecken. Funktionen kontrollerar filstorlek och avkodar UTF-8. Den använder sedan standardbibliotekets `csv.reader` för att kontrollera att rubrikerna är ifyllda och unika och att raderna har lika många fält. Det extra steget behövs eftersom Pandas annars kan tolka vissa ojämna rader utan att stoppa inläsningen.

`pd.read_csv()` skapar därefter en DataFrame. Tomma filer, fel i CSV-strukturen och filer utan datarader ger `ValueError` med ett begripligt meddelande. `main()` fångar det felet och visar texten med `st.error`. Tomma fält i en i övrigt korrekt rad är tillåtna och räknas som saknade värden.

### Datakvalitet och statistik

`summarize_columns()` bygger en ny tabell med datatyper, antal saknade värden och procentandelar. Ursprungstabellen ändras inte. Översikten gäller hela datasetet, medan `data[selected]` begränsar förhandsgranskning, statistik och diagram till användarens val.

`describe(include="all")` sammanfattar både text och numeriska kolumner. Resultatet omvandlas till strängar vid visning för att blandade typer i statistiktabellen ska kunna visas stabilt. Det påverkar inte ursprungliga värden eller beräkningar.

### Visualisering

`show_charts()` använder `select_dtypes(include="number")` för att hitta numeriska kolumner. Användaren väljer en av dem. Saknade och oändliga värden utelämnas från en separat diagramserie. Därefter skapas histogrammet och lådagrammet med Plotly Express. Om inga användbara tal finns visas ett meddelande i stället för tomma diagram.

## 7. Resultat och demonstration

Den färdiga lösningen innehåller filuppladdning, tabeller, statistik, kolumnval och två numeriska visualiseringar. Detaljer om faktiskt genomförd verifiering finns i `TEST_RESULTS.md`.

Exempelfilen innehåller 12 produkter och fyra kolumner. Det finns ett saknat värde i kategori, pris respektive antal. För pris blir antalet ifyllda värden 11, medianen 79 och medelvärdet cirka 85,91. Skillnaden mellan median och medelvärde illustrerar att högre värden kan påverka medelvärdet.

Vid en demonstration kan exempeldata först öppnas, därefter kan tabellen över saknade värden visas. Välj pris och förklara histogrammet och lådagrammet. Byt sedan till antal för att visa att gränssnittet uppdateras. Avsluta med att välja enbart textkolumner och visa det begripliga meddelandet.

**Egen demonstration:** [Fyll i när du själv har genomfört demonstrationen och vad du observerade.]

## 8. Problem, begränsningar och förbättringar

CSV är enkelt men filer kan ha olika avgränsare, decimaltecken och teckenkodningar. Lösningen låter användaren välja avgränsare och decimaltecken men kräver UTF-8. Fel avgränsare kan fortfarande ge en tekniskt giltig tabell med en kolumn. Därför visar appen en upplysning i det läget.

Automatisk typbestämning kan tolka en blandad kolumn som text. Markören `NA` kan vara en giltig kategori i vissa dataset men tolkas normalt som saknad. Sådana val behöver analyseras utifrån datans betydelse. Projektet försöker inte rätta detta automatiskt.

All data läses i minnet vid varje omkörning, vilket begränsar skalbarheten. Möjliga förbättringar är cachelagring för större filer, explicit val av saknade-värden-markörer och typomvandling med tydlig återkoppling. Ett spridningsdiagram mellan två numeriska kolumner är ett naturligt nästa analyssteg. Dessa funktioner ingår inte i den aktuella lösningen.

## 9. Källor

Officiell dokumentation kontrollerad 12 oktober 2026. Dokumentationens aktuella version kan skilja sig från lokalt installerade versioner; testmiljön anges i testprotokollet.

- [Streamlit: st.file_uploader](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader) – uppladdaren och det filliknande returvärdet.
- [Streamlit: AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest) – simulerad körning och granskning av appens element.
- [Pandas: read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) – CSV-inläsning, avgränsare och decimaltecken.
- [Pandas: DataFrame.isna](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.isna.html) – identifiering av saknade värden.
- [Pandas: DataFrame.describe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html) – numerisk och kategorisk sammanfattning.
- [Plotly: histogram](https://plotly.com/python/histograms/) – frekvensdiagram med Plotly Express.
- [Plotly: lådagram](https://plotly.com/python/box-plots/) – median, kvartiler och spröt.

## 10. Självreflektion – fyll i själv

Detta avsnitt ska bygga på dina egna erfarenheter. Förslagen nedan är frågor att utgå från, inte påståenden om vad du har lärt dig.

**Vad lärde jag mig som jag inte kunde innan?**  
[Beskriv ett konkret exempel. Kan du nu förklara hur CSV blir en DataFrame, hur isna fungerar eller varför Streamlit kör om skriptet?]

**Vad var svårast att förstå eller genomföra?**  
[Beskriv ett verkligt problem, hur du undersökte det och vad som hjälpte.]

**Vilket tekniskt val är jag mest nöjd med och varför?**  
[Välj ett val du själv förstår, exempelvis separat inläsningsfunktion eller två diagram för samma variabel. Beskriv en fördel och en begränsning.]

**Vad hade jag gjort annorlunda om jag började om?**  
[Utgå från ditt faktiska arbete. Vad skulle du testa tidigare eller strukturera annorlunda?]

**Vad skulle vara ett naturligt nästa steg?**  
[Välj en avgränsad förbättring och förklara varför den vore användbar.]

**Vilket betyg tycker jag att arbetet motsvarar, G eller VG?**  
[Fyll i din egen bedömning efter att ha läst kursens fullständiga kriterier. Målet för detta projekt är G. Inga VG-kriterier har funnits i underlaget.]

**Hur motiverar jag bedömningen utifrån kursens betygskriterier?**  
[Klistra in eller sammanfatta de faktiska kriterierna. Koppla vart och ett till kod, testresultat, rapport eller din muntliga förklaring. Funktionskraven i beställningen är inte en ersättning för kursens betygsmatris.]
