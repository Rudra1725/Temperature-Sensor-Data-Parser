import os
import csv
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SensorParserApp(ctk.CTk):
    def __init__(r):
        super().__init__()

        r.title("Temperature Sensor Data Parser")
        r.geometry("1020, 680")
        r.minsize(940, 600)

        r.valid_readings = []
        r.parsed_records = []
        r.temp_threshold = 30.0

        r.grid_columnconfigure(0, weight=1)
        r.grid_rowconfigure(2, weight=1)

        r._create_header()
        r._create_toolbar()
        r._create_main_content()
        r._create_footer()

    def _create_header(r):
        header_frame = ctk.CTkFrame(r, corner_radius=12, fg_color="#1f232a")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame,
            text="Temperature Sensor Data Parser",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#ffffff"
        )
        title.grid(row=0, column=0, padx=20, pady=(15, 2), sticky="w")

        info_btn = ctk.CTkButton(
            header_frame,
            text="ⓘ",
            width=32,
            height=32,
            corner_radius=16,
            fg_color="#2b313a",
            hover_color="#38404c",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=r.show_developer_info
        )
        info_btn.grid(row=0, column=1, rowspan=2, padx=20, pady=15, sticky="e")

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Raw hardware log ingestion, normalization, and statistical analysis",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#9ba1a6"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

    def show_developer_info(r):
        info_dialog = ctk.CTkToplevel(r)
        info_dialog.title("Developer Information")
        info_dialog.geometry("380, 260")
        info_dialog.resizable(False, False)
        info_dialog.transient(r)
        info_dialog.grab_set()

        dialog_frame = ctk.CTkFrame(info_dialog, fg_color="#1b1d22", corner_radius=10)
        dialog_frame.pack(fill="both", expand=True, padx=15, pady=15)

        title_lbl = ctk.CTkLabel(
            dialog_frame,
            text="Project Developer",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        )
        title_lbl.pack(pady=(15, 5))

        dev_lbl = ctk.CTkLabel(
            dialog_frame,
            text="Rudra Wagh",
            font=ctk.CTkFont(family="Segoe UI", size=15),
            text_color="#58a6ff"
        )
        dev_lbl.pack(pady=(0, 15))

        btn_container = ctk.CTkFrame(dialog_frame, fg_color="transparent")
        btn_container.pack(fill="x", padx=30, pady=5)

        gh_btn = ctk.CTkButton(
            btn_container,
            text="GitHub Profile",
            height=35,
            fg_color="#238636",
            hover_color="#2ea043",
            font=ctk.CTkFont(weight="bold"),
            command=lambda: webbrowser.open("https://github.com/Rudra1725")
        )
        gh_btn.pack(fill="x", pady=5)

        li_btn = ctk.CTkButton(
            btn_container,
            text="LinkedIn Profile",
            height=35,
            fg_color="#0077b5",
            hover_color="#005885",
            font=ctk.CTkFont(weight="bold"),
            command=lambda: webbrowser.open("https://www.linkedin.com/in/rudra-wagh-476a9830b")
        )
        li_btn.pack(fill="x", pady=5)

    def _create_toolbar(r):
        toolbar = ctk.CTkFrame(r, fg_color="transparent")
        toolbar.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        toolbar.grid_columnconfigure(0, weight=1)

        r.file_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="No file selected...",
            height=38,
            font=ctk.CTkFont(size=13)
        )
        r.file_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        browse_btn = ctk.CTkButton(
            toolbar,
            text="Browse Log File",
            height=38,
            width=120,
            command=r.browse_file
        )
        browse_btn.grid(row=0, column=1, padx=(0, 10))

        parse_btn = ctk.CTkButton(
            toolbar,
            text="Parse Data",
            height=38,
            width=110,
            fg_color="#238636",
            hover_color="#2ea043",
            command=r.parse_logs
        )
        parse_btn.grid(row=0, column=2, padx=(0, 10))

        r.export_btn = ctk.CTkButton(
            toolbar,
            text="Export CSV",
            height=38,
            width=110,
            fg_color="#1f6feb",
            hover_color="#388bfd",
            command=r.export_to_csv
        )
        r.export_btn.grid(row=0, column=3)

    def _create_main_content(r):
        content_frame = ctk.CTkFrame(r, fg_color="transparent")
        content_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        r.output_textbox = ctk.CTkTextbox(
            content_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="none",
            corner_radius=10
        )
        r.output_textbox.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        stats_panel = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#181a1f")
        stats_panel.grid(row=0, column=1, sticky="nsew")

        stats_title = ctk.CTkLabel(
            stats_panel,
            text="Telemetry Summary",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        stats_title.pack(padx=15, pady=(20, 10), anchor="w")

        r.stat_count = r._add_stat_row(stats_panel, "Readings Parsed", "--")
        r.stat_avg = r._add_stat_row(stats_panel, "Average Temp", "--")
        r.stat_min = r._add_stat_row(stats_panel, "Minimum Temp", "--")
        r.stat_max = r._add_stat_row(stats_panel, "Maximum Temp", "--")

        threshold_box = ctk.CTkFrame(stats_panel, fg_color="#22252c", corner_radius=8)
        threshold_box.pack(fill="x", padx=15, pady=(15, 6))

        thresh_lbl = ctk.CTkLabel(
            threshold_box,
            text="Alert Threshold (°C)",
            font=ctk.CTkFont(size=12),
            text_color="#8b949e"
        )
        thresh_lbl.pack(anchor="w", padx=12, pady=(8, 2))

        r.thresh_entry = ctk.CTkEntry(
            threshold_box,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        r.thresh_entry.insert(0, "30.0")
        r.thresh_entry.pack(fill="x", padx=12, pady=(0, 8))

    def _add_stat_row(r, parent, label_text, default_val):
        frame = ctk.CTkFrame(parent, fg_color="#22252c", corner_radius=8)
        frame.pack(fill="x", padx=15, pady=6)

        lbl = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(size=12), text_color="#8b949e")
        lbl.pack(anchor="w", padx=12, pady=(8, 0))

        val = ctk.CTkLabel(frame, text=default_val, font=ctk.CTkFont(size=16, weight="bold"))
        val.pack(anchor="w", padx=12, pady=(0, 8))
        return val

    def _create_footer(r):
        footer_frame = ctk.CTkFrame(r, height=45, fg_color="#131519", corner_radius=0)
        footer_frame.grid(row=3, column=0, sticky="ew")

        r.status_lbl = ctk.CTkLabel(
            footer_frame,
            text="Ready to load telemetry streams",
            font=ctk.CTkFont(size=12),
            text_color="#8b949e"
        )
        r.status_lbl.pack(side="left", padx=20)

    def browse_file(r):
        file_path = filedialog.askopenfilename(
            filetypes=[("Log & Text Files", "*.txt *.log"), ("All Files", "*.*")]
        )
        if file_path:
            r.file_entry.delete(0, "end")
            r.file_entry.insert(0, file_path)

    def convert_to_celsius(r, value, unit):
        if unit == "C":
            return value
        elif unit == "F":
            return (value - 32.0) * (5.0 / 9.0)
        elif unit == "K":
            return value - 273.15
        return None

    def parse_logs(r):
        filename = r.file_entry.get().strip()
        if not filename or not os.path.exists(filename):
            messagebox.showerror("File Error", "Please specify a valid file path to parse.")
            return

        try:
            r.temp_threshold = float(r.thresh_entry.get().strip())
        except ValueError:
            r.temp_threshold = 30.0
            r.thresh_entry.delete(0, "end")
            r.thresh_entry.insert(0, "30.0")

        r.output_textbox.delete("1.0", "end")
        r.valid_readings.clear()
        r.parsed_records.clear()

        high_temp_alerts = []

        header_str = f"{'Timestamp':<20} | {'Sensor ID':<12} | {'Temp (°C)':<12} | {'Status'}\n"
        divider = "-" * 62 + "\n"
        r.output_textbox.insert("end", header_str)
        r.output_textbox.insert("end", divider)

        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(" | ")
                    if len(parts) < 4:
                        continue

                    timestamp = parts[0]
                    sensor_id = parts[1].split(":")[1]
                    raw_field = parts[2].split(":")[1]
                    status = parts[3].split(":")[1]

                    if status != "OK" or raw_field in ("INVALID", "NAN", "TIMEOUT", "NULL"):
                        r.output_textbox.insert(
                            "end",
                            f"{timestamp:<20} | {sensor_id:<12} | {'N/A':<12} | DISCARDED\n"
                        )
                        r.parsed_records.append([timestamp, sensor_id, "N/A", "DISCARDED"])
                        continue

                    unit = raw_field[-1].upper()
                    numeric_str = raw_field[:-1]

                    try:
                        raw_temp = float(numeric_str)
                        celsius = r.convert_to_celsius(raw_temp, unit)
                        if celsius is not None:
                            r.valid_readings.append(celsius)
                            status_tag = "VALID"
                            
                            if celsius >= r.temp_threshold:
                                status_tag = "HIGH_TEMP"
                                high_temp_alerts.append((timestamp, sensor_id, celsius))

                            r.output_textbox.insert(
                                "end",
                                f"{timestamp:<20} | {sensor_id:<12} | {celsius:<12.2f} | {status_tag}\n"
                            )
                            r.parsed_records.append([timestamp, sensor_id, f"{celsius:.2f}", status_tag])
                    except ValueError:
                        r.output_textbox.insert(
                            "end",
                            f"{timestamp:<20} | {sensor_id:<12} | {'ERROR':<12} | PARSE_FAILED\n"
                        )
                        r.parsed_records.append([timestamp, sensor_id, "ERROR", "PARSE_FAILED"])

            r.update_statistics()
            r.status_lbl.configure(text=f"Processed {len(r.parsed_records)} rows | {len(r.valid_readings)} valid readings")

            if high_temp_alerts:
                highest = max(high_temp_alerts, key=lambda x: x[2])
                messagebox.showwarning(
                    "Threshold Breach Detected",
                    f"Warning: {len(high_temp_alerts)} readings exceeded {r.temp_threshold} °C!\n\n"
                    f"Max reading observed:\nSensor: {highest[1]}\nTemp: {highest[2]:.2f} °C\nTime: {highest[0]}"
                )

        except Exception as e:
            messagebox.showerror("Execution Error", f"An error occurred while parsing:\n{str(e)}")

    def export_to_csv(r):
        if not r.parsed_records:
            messagebox.showwarning("Export Notice", "No parsed telemetry available to export. Run 'Parse Data' first.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            initialfile="parsed_telemetry.csv"
        )

        if not save_path:
            return

        try:
            with open(save_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Timestamp", "Sensor_ID", "Normalized_Temp_Celsius", "Status"])
                writer.writerows(r.parsed_records)

            messagebox.showinfo("Export Successful", f"Telemetry successfully saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to save CSV file:\n{str(e)}")

    def update_statistics(r):
        if r.valid_readings:
            avg_temp = sum(r.valid_readings) / len(r.valid_readings)
            min_temp = min(r.valid_readings)
            max_temp = max(r.valid_readings)

            r.stat_count.configure(text=str(len(r.valid_readings)))
            r.stat_avg.configure(text=f"{avg_temp:.2f} °C")
            r.stat_min.configure(text=f"{min_temp:.2f} °C")
            r.stat_max.configure(text=f"{max_temp:.2f} °C")
        else:
            r.stat_count.configure(text="0")
            r.stat_avg.configure(text="--")
            r.stat_min.configure(text="--")
            r.stat_max.configure(text="--")

if __name__ == "__main__":
    app = SensorParserApp()
    app.mainloop()
