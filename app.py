"""En liten Streamlit-app för att utforska CSV-filer."""

import csv
from io import StringIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


MAX_FILE_BYTES = 10 * 1024 * 1024


def load_csv(content: bytes, separator: str = ",", decimal: str = ".") -> pd.DataFrame:
    """Läs UTF-8-data och ge begripliga fel vid ogiltiga filer."""
    if len(content) > MAX_FILE_BYTES:
        raise ValueError("Filen är för stor. Välj en CSV-fil på högst 10 MB.")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError("Filen måste vara sparad som UTF-8. Exportera den som CSV UTF-8.") from error
    if not text.strip():
        raise ValueError("Filen är tom. Välj en fil med kolumnrubriker och datarader.")
    if "\x00" in text:
        raise ValueError("Filen innehåller ogiltiga tecken. Kontrollera att den är en CSV-textfil.")

    # Kontrollera även korta rader; Pandas kan annars fylla ut dem utan fel.
    try:
        rows = csv.reader(StringIO(text), delimiter=separator, strict=True)
        header = None
        for row in rows:
            if not row:
                continue
            if header is None:
                header = row
                if any(not name.strip() for name in header) or len(set(header)) != len(header):
                    raise ValueError("Kolumnrubriker måste vara ifyllda och unika.")
            elif len(row) != len(header):
                raise ValueError("Raderna har olika antal fält. Kontrollera avgränsare och citattecken.")
        data = pd.read_csv(StringIO(text), sep=separator, decimal=decimal)
    except (csv.Error, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
        raise ValueError("CSV-filen kunde inte läsas. Kontrollera avgränsare och citattecken.") from error
    if data.empty:
        raise ValueError("Filen innehåller inga datarader. Lägg till data under rubrikerna.")
    return data


def summarize_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Sammanställ datatyper och saknade värden per kolumn."""
    return pd.DataFrame({
        "Datatyp": data.dtypes.astype(str),
        "Saknade värden": data.isna().sum(),
        "Saknade (%)": (data.isna().mean() * 100).round(1),
    }).rename_axis("Kolumn")


def show_charts(data: pd.DataFrame) -> None:
    """Visa fördelningen för en vald numerisk kolumn på två sätt."""
    numeric_columns = data.select_dtypes(include="number").columns.tolist()
    if not numeric_columns:
        st.info("De valda kolumnerna saknar numeriska data. Välj en numerisk kolumn för att visa diagram.")
        return
    column = st.selectbox("Numerisk kolumn för diagram", numeric_columns)
    # Diagram behöver ändliga värden. Ursprunglig data ändras inte.
    values = data[column].replace([float("inf"), float("-inf")], float("nan")).dropna()
    st.caption(f"Diagrammen använder {len(values)} värden. {len(data) - len(values)} saknade eller oändliga värden utelämnas.")
    if values.empty:
        st.warning("Kolumnen saknar ändliga numeriska värden att visa.")
        return
    chart_data = values.to_frame()
    st.plotly_chart(px.histogram(chart_data, x=column, title=f"Histogram – {column}",
                                 labels={column: column}), width="stretch")
    st.caption("Histogrammet visar hur många värden som finns inom olika intervall.")
    st.plotly_chart(px.box(chart_data, y=column, title=f"Lådagram – {column}"), width="stretch")
    st.caption("Lådan visar de mittersta 50 procenten och linjen visar medianen. Punkter utanför spröten är möjliga avvikare, inte automatiskt fel.")


def main() -> None:
    st.set_page_config(page_title="CSV-utforskaren", layout="wide")
    st.title("CSV-utforskaren")
    st.write("Ladda upp en CSV-fil och undersök innehåll, saknade värden och fördelningar.")
    uploaded_file = st.file_uploader("Välj en CSV-fil (UTF-8, högst 10 MB)", type=["csv"])
    use_sample = st.checkbox("Använd exempeldata", value=False)
    separator_label = st.selectbox("Avgränsare", ["Komma (,)", "Semikolon (;)", "Tabb"])
    separator = {"Komma (,)": ",", "Semikolon (;)": ";", "Tabb": "\t"}[separator_label]
    decimal = st.selectbox("Decimaltecken", [".", ","])

    try:
        if use_sample:
            data = load_csv(Path(__file__).with_name("sample_data.csv").read_bytes())
            st.caption("Visar påhittade exempeldata. Filinställningarna används endast för uppladdade filer.")
        elif uploaded_file is not None:
            data = load_csv(uploaded_file.getvalue(), separator, decimal)
        else:
            st.info("Ladda upp en fil eller välj exempeldata för att börja.")
            return
    except (ValueError, OSError) as error:
        st.error(str(error))
        return

    if len(data.columns) == 1:
        st.info("Filen lästes som en kolumn. Om du väntade dig fler, kontrollera avgränsaren.")
    left, right = st.columns(2)
    left.metric("Antal rader", len(data))
    right.metric("Antal kolumner", len(data.columns))
    st.subheader("Kolumner och saknade värden – hela datasetet")
    st.dataframe(summarize_columns(data), width="stretch")
    st.caption("Tomma fält och Pandas standardmarkörer, exempelvis NA, tolkas som saknade värden. Inga värden fylls i automatiskt.")

    selected = st.multiselect("Kolumner att utforska", data.columns.tolist(), default=data.columns.tolist())
    if not selected:
        st.info("Välj minst en kolumn för att visa data, statistik och diagram.")
        return
    selected_data = data[selected]
    st.subheader("Förhandsgranskning – högst 20 rader")
    st.dataframe(selected_data.head(20), width="stretch")
    st.subheader("Beskrivande statistik – valda kolumner")
    # Strängformat gör tabellen visningsbar även när tal och text blandas.
    st.dataframe(selected_data.describe(include="all").astype(str), width="stretch")
    st.caption("count = antal ifyllda värden, mean = medelvärde, std = standardavvikelse, 50% = median. För text visas unique, top och freq. NaN betyder att måttet saknas eller inte är tillämpligt.")
    st.subheader("Visualiseringar – valda kolumner")
    show_charts(selected_data)


if __name__ == "__main__":
    main()
