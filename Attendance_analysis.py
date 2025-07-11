import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, time
from fpdf import FPDF
from PIL import Image
import io
import tempfile
import os
import altair_saver

st.set_page_config("📊 Attendance Dashboard", layout="wide")
st.title("📊 Employee Attendance Dashboard")

# Automatically load 'ExportedTable.xlsx' from Documents
documents_folder = os.path.expanduser("~/Documents")
file_path = os.path.join(documents_folder, "ExportedTable.xlsx")

if os.path.exists(file_path):
    st.success(f"📁 Loaded file: {file_path}")
    try:
        df = pd.read_excel(file_path)


        required_cols = ['Name', 'Timein', 'Timeout']
        for col in required_cols:
            if col not in df.columns:
                st.error(f"❌ Missing required column: '{col}'")
                st.stop()

        df['Timeout'] = pd.to_datetime(df['Timeout'])

        def parse_timein(row):
            try:
                if isinstance(row['Timein'], time):
                    if row['Timeout'].time() < time(12, 0):
                        return None
                    return datetime.combine(row['Timeout'].date(), row['Timein'])
                parsed_time = pd.to_datetime(str(row['Timein'])).time()
                if row['Timeout'].time() < time(12, 0):
                    return None
                return datetime.combine(row['Timeout'].date(), parsed_time)
            except:
                return None

        df['Timein_dt'] = df.apply(parse_timein, axis=1)
        df['Signed In Only'] = df['Timein_dt'].isna()

        def get_arrival(row):
            if pd.isna(row['Timein_dt']):
                return None
            return 'Late' if row['Timein_dt'].time() > time(9, 0) else 'Early'

        df['Arrival'] = df.apply(get_arrival, axis=1)

        def get_closure(row):
            if pd.isna(row['Timeout']):
                return None
            return 'Left Early' if row['Timeout'].time() < time(15, 30) else 'Stayed Till Close'

        df['Closure Status'] = df.apply(get_closure, axis=1)

        st.sidebar.header("📅 Filter by Date")
        min_date = df['Timeout'].min().date()
        max_date = df['Timeout'].max().date()
        start_date, end_date = st.sidebar.date_input("Select date range:", [min_date, max_date])

        df_filtered = df[
            (df['Timeout'].dt.date >= start_date) &
            (df['Timeout'].dt.date <= end_date)
        ]

        st.caption(f"Showing records from **{start_date}** to **{end_date}**")

        appearances = df_filtered[~df_filtered['Signed In Only']]['Name'].value_counts().reset_index()
        appearances.columns = ['Name', 'Appearances']
        chart1 = alt.Chart(appearances).mark_bar().encode(
            x='Appearances:Q',
            y=alt.Y('Name:N', sort='-x'),
            tooltip=['Name', 'Appearances']
        ).properties(width=600, height=400)
        st.altair_chart(chart1, use_container_width=True)

        unsigned_out = df_filtered[df_filtered['Signed In Only']]['Name'].value_counts().reset_index()
        unsigned_out.columns = ['Name', 'Missed Sign-Outs']
        chart2 = alt.Chart(unsigned_out).mark_bar(color='red').encode(
            x='Missed Sign-Outs:Q',
            y=alt.Y('Name:N', sort='-x'),
            tooltip=['Name', 'Missed Sign-Outs']
        ).properties(width=600, height=400)
        if not unsigned_out.empty:
            st.altair_chart(chart2, use_container_width=True)

        arrival_stats = df_filtered[~df_filtered['Signed In Only']].groupby(['Name', 'Arrival']).size().unstack().fillna(0)
        for col in ['Early', 'Late']:
            if col not in arrival_stats.columns:
                arrival_stats[col] = 0
        arrival_stats = arrival_stats.reset_index()
        arrival_melt = arrival_stats.melt(id_vars='Name', var_name='Arrival', value_name='Count')
        chart3 = alt.Chart(arrival_melt).mark_bar().encode(
            x='Count:Q',
            y=alt.Y('Name:N', sort='-x'),
            color=alt.Color('Arrival:N', scale=alt.Scale(domain=['Early', 'Late'], range=['green', 'orange'])),
            tooltip=['Name', 'Arrival', 'Count']
        ).properties(width=700, height=400)
        st.altair_chart(chart3, use_container_width=True)

        closure_stats = df_filtered[~df_filtered['Signed In Only']].groupby(['Name', 'Closure Status']).size().unstack().fillna(0)
        for col in ['Left Early', 'Stayed Till Close']:
            if col not in closure_stats.columns:
                closure_stats[col] = 0
        closure_stats = closure_stats.reset_index()
        closure_melt = closure_stats.melt(id_vars='Name', var_name='Closure Status', value_name='Count')
        chart4 = alt.Chart(closure_melt).mark_bar().encode(
            x='Count:Q',
            y=alt.Y('Name:N', sort='-x'),
            color=alt.Color('Closure Status:N', scale=alt.Scale(domain=['Left Early', 'Stayed Till Close'], range=['red', 'blue'])),
            tooltip=['Name', 'Closure Status', 'Count']
        ).properties(width=700, height=400)
        st.altair_chart(chart4, use_container_width=True)

        def summarize_behavior(subdf):
            arrival_mode = subdf['Arrival'].mode().iloc[0] if not subdf['Arrival'].dropna().empty else "N/A"
            closure_mode = subdf['Closure Status'].mode().iloc[0] if not subdf['Closure Status'].dropna().empty else "N/A"
            return pd.Series({'Usual Arrival': arrival_mode, 'Usual Closure': closure_mode})

        summary = df_filtered[~df_filtered['Signed In Only']].groupby('Name').apply(summarize_behavior).reset_index()
        st.dataframe(summary)

        def save_chart_image(chart, filename):
            path = os.path.join(tempfile.gettempdir(), filename)
            altair_saver.save(chart, path)
            return path

        st.subheader("📤 Export Full Dashboard to PDF")

        if st.button("Generate Full PDF Report"):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(190, 10, "Full Attendance Dashboard", ln=True, align='C')
            pdf.set_font("Arial", size=11)
            pdf.cell(190, 10, f"Date Range: {start_date} to {end_date}", ln=True)
            pdf.ln(5)

            # Save charts as images and insert
            for idx, (chart, title) in enumerate([
                (chart1, "Appearance Count"),
                (chart2, "Missed Sign-Outs"),
                (chart3, "Early vs Late"),
                (chart4, "Closure Status")
            ]):
                if chart:
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(190, 10, title, ln=True)
                    img_path = save_chart_image(chart, f"chart_{idx}.png")
                    pdf.image(img_path, x=10, y=30, w=180)

            # Add summary table
            pdf.add_page()
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(60, 10, "Name", 1)
            pdf.cell(60, 10, "Usual Arrival", 1)
            pdf.cell(60, 10, "Usual Closure", 1)
            pdf.ln()
            pdf.set_font("Arial", size=11)
            for _, row in summary.iterrows():
                pdf.cell(60, 10, str(row['Name']), 1)
                pdf.cell(60, 10, str(row['Usual Arrival']), 1)
                pdf.cell(60, 10, str(row['Usual Closure']), 1)
                pdf.ln()

            pdf_output = io.BytesIO(pdf.output(dest='S').encode('latin1'))

            st.download_button(
                label="📄 Download Full Dashboard PDF",
                data=pdf_output,
                file_name=f"Full_Attendance_Dashboard_{start_date}_to_{end_date}.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📥 Please upload an Excel file with columns: Name, Timein, Timeout")
