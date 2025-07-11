import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fpdf import FPDF
from datetime import datetime, time
import os

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Attendance Dashboard")
        self.root.geometry("1200x800")

        self.data = None
        self.filtered_data = None
        self.summary_df = None
        self.last_dir = os.getcwd()

        self.create_widgets()

    def create_widgets(self):
        # File Upload
        upload_btn = tk.Button(self.root, text="Upload Excel File", command=self.load_file)
        upload_btn.pack(pady=10)

        # Date Range
        date_frame = tk.Frame(self.root)
        tk.Label(date_frame, text="Start Date:").pack(side=tk.LEFT)
        self.start_date = DateEntry(date_frame)
        self.start_date.pack(side=tk.LEFT, padx=5)

        tk.Label(date_frame, text="End Date:").pack(side=tk.LEFT)
        self.end_date = DateEntry(date_frame)
        self.end_date.pack(side=tk.LEFT, padx=5)

        filter_btn = tk.Button(date_frame, text="Apply Filter", command=self.filter_data)
        filter_btn.pack(side=tk.LEFT, padx=10)
        date_frame.pack(pady=10)

        # Plot Area
        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.pack()

        # Summary Table
        self.summary_table = ttk.Treeview(self.root, columns=("Name", "Arrival", "Closure"), show="headings")
        self.summary_table.heading("Name", text="Name")
        self.summary_table.heading("Arrival", text="Usual Arrival")
        self.summary_table.heading("Closure", text="Usual Closure")
        self.summary_table.pack(pady=10, fill=tk.BOTH, expand=True)

        # Export to PDF
        export_btn = tk.Button(self.root, text="Export to PDF", command=self.export_pdf)
        export_btn.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(initialdir=self.last_dir, filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                self.last_dir = os.path.dirname(file_path)
                df = pd.read_excel(file_path)

                # Clean column names
                df.columns = df.columns.str.strip().str.lower()

                # Ensure necessary columns exist
                required_cols = ['name', 'timein', 'timeout']
                for col in required_cols:
                    if col not in df.columns:
                        raise Exception(f"Missing column: {col}")

                df['timeout'] = pd.to_datetime(df['timeout'], errors='coerce')

                # Safely combine date + time
                def safe_combine(row):
                    if pd.notna(row['timein']) and isinstance(row['timein'], time) and pd.notna(row['timeout']):
                        try:
                            if row['timeout'].time() >= time(12, 0):
                                return datetime.combine(row['timeout'].date(), row['timein'])
                        except Exception:
                            return None
                    return None

                df['timein_dt'] = df.apply(safe_combine, axis=1)
                df['signed_in_only'] = df['timein_dt'].isna()
                df['arrival'] = df['timein_dt'].apply(lambda t: 'Late' if pd.notna(t) and t.time() > time(9, 0) else 'Early')
                df['closure_status'] = df['timeout'].apply(lambda t: 'Left Early' if pd.notna(t) and t.time() < time(15, 30) else 'Stayed Till Close')

                self.data = df
                messagebox.showinfo("Success", "File loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def filter_data(self):
        if self.data is None:
            messagebox.showerror("Error", "Please upload a file first.")
            return

        start = self.start_date.get_date()
        end = self.end_date.get_date()

        df = self.data.copy()
        df = df[(df['timeout'].dt.date >= start) & (df['timeout'].dt.date <= end)]
        self.filtered_data = df

        self.plot_charts(df)
        self.populate_summary(df)

    def plot_charts(self, df):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig, axs = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)

        # Appearance Count
        df[~df['signed_in_only']]['name'].value_counts().plot(kind='barh', ax=axs[0, 0], color='skyblue')
        axs[0, 0].set_title("Appearance Count")

        # Missed Sign-outs
        df[df['signed_in_only']]['name'].value_counts().plot(kind='barh', ax=axs[0, 1], color='red')
        axs[0, 1].set_title("Missed Sign-Outs")

        # Early vs Late
        df.groupby(['name', 'arrival']).size().unstack(fill_value=0).plot(kind='barh', stacked=True, ax=axs[1, 0], color=['green', 'orange'])
        axs[1, 0].set_title("Early vs Late")

        # Closure Status
        df.groupby(['name', 'closure_status']).size().unstack(fill_value=0).plot(kind='barh', stacked=True, ax=axs[1, 1], color=['red', 'blue'])
        axs[1, 1].set_title("Closure Status")

        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def populate_summary(self, df):
        for row in self.summary_table.get_children():
            self.summary_table.delete(row)

        summary = df[~df['signed_in_only']].groupby('name').agg(
            usual_arrival=('arrival', lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A'),
            usual_closure=('closure_status', lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A')
        ).reset_index()

        for _, row in summary.iterrows():
            self.summary_table.insert('', tk.END, values=(row['name'], row['usual_arrival'], row['usual_closure']))

        self.summary_df = summary

    def export_pdf(self):
        if self.filtered_data is None or self.summary_df is None:
            messagebox.showerror("Error", "Please load and filter data first.")
            return

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, "Attendance Report", ln=True, align='C')
        pdf.ln(5)

        # Add date range
        start = self.start_date.get_date()
        end = self.end_date.get_date()
        pdf.cell(200, 10, f"Date Range: {start} to {end}", ln=True)
        pdf.ln(5)

        # Add summary
        pdf.cell(200, 10, "Summary Table:", ln=True)
        for _, row in self.summary_df.iterrows():
            pdf.cell(200, 10, f"{row['name']} - {row['usual_arrival']} / {row['usual_closure']}", ln=True)

        output_path = filedialog.asksaveasfilename(initialdir=self.last_dir, defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output_path:
            try:
                pdf.output(output_path)
                messagebox.showinfo("Success", f"PDF saved to {output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PDF: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
