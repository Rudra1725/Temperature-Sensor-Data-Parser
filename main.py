import os
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SensorParserApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Temperature Sensor Data Parser")
        self.geometry("920, 680")
        self.minsize(850, 600)

        self.valid_readings = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._create_header()
        self._create_toolbar()
        self._create_main_content()
        self._create_footer()

    def _create_header(self):
        header_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1f232a")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame,
            text="Temperature Sensor Data Parser",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#ffffff"
        )
        title.grid(row=0, column=0, padx=20, pady=(15, 2), sticky="w")

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Raw hardware log ingestion, normalization, and statistical analysis",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#9ba1a6"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

    def _create_toolbar(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        toolbar.grid_columnconfigure(0, weight=1)

        self.file_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="No file selected...",
            height=38,
            font=ctk.CTkFont(size=13)
        )
        self.file_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        browse_btn = ctk.CTkButton(
            toolbar,
            text="Browse Log File",
            height=38,
            width=130,
            command=self.browse_file
        )
        browse_btn.grid(row=0, column=1, padx=(0, 10))

        parse_btn = ctk.CTkButton(
            toolbar,
            text="Parse Data",
            height=38,
            width=120,
            fg_color="#238636",
            hover_color="#2ea043",
            command=self.parse_logs
        )
        parse_btn.grid(row=0, column=2)

    def _create_main_content(self):
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        self.output_textbox = ctk.CTkTextbox(
            content_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="none",
            corner_radius=10
        )
        self.output_textbox.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        stats_panel = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#181a1f")
        stats_panel.grid(row=0, column=1, sticky="nsew")

        stats_title = ctk.CTkLabel(
            stats_panel,
            text="Telemetry Summary",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        stats_title.pack(padx=15, pady=(20, 15), anchor="w")

        self.stat_count = self._add_stat_row(stats_panel, "Readings Parsed", "--")
        self.stat_avg = self._add_stat_row(stats_panel, "Average Temp", "--")
        self.stat_min = self._add_stat_row(stats_panel, "Minimum Temp", "--")
        self.stat_max = self._add_stat_row(stats_panel, "Maximum Temp", "--")

    def _add_stat_row(self, parent, label_text, default_val):
        frame = ctk.CTkFrame(parent, fg_color="#22252c", corner_radius=8)
        frame.pack(fill="x", padx=15, pady=6)

        lbl = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(size=12), text_color="#8b949e")
        lbl.pack(anchor="w", padx=12, pady=(8, 0))

        val = ctk.CTkLabel(frame, text=default_val, font=ctk.CTkFont(size=16, weight="bold"))
        val.pack(anchor="w", padx=12, pady=(0, 8))
        return val

    def _create_footer(self):
        footer_frame = ctk.CTkFrame(self, height=45, fg_color="#131519", corner_radius=0)
        footer_frame.grid(row=3, column=0, sticky="ew")

        dev_label = ctk.CTkLabel(
            footer_frame,
            text="Developed by Rudra Wagh",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#c9d1d9"
        )
        dev_label.pack(side="left", padx=20)

        github_btn = ctk.CTkButton(
            footer_frame,
            text="GitHub",
            width=70,
            height=26,
            fg_color="#21262d",
            hover_color="#30363d",
            command=lambda: webbrowser.open("https://github.com/Rudra1725")
        )
        github_btn.pack(side="right", padx=(0, 20), pady=8)

        linkedin_btn = ctk.CTkButton(
            footer_frame,
            text="LinkedIn",
            width=70,
            height=26,
            fg_color="#0077b5",
            hover_color="#005885",
            command=lambda: webbrowser.open("https://www.linkedin.com/in/rudra-wagh-476a9830b")
        )
        linkedin_btn.pack(side="right", padx=(0, 10), pady=8)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Log & Text Files", "*.txt *.log"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, file_path)

    def convert_to_celsius(self, value, unit):
        if unit == "C":
            return value
        elif unit == "F":
            return (value - 32.0) * (5.0 / 9.0)
        elif unit == "K":
            return value - 273.15
        return None

    def parse_logs(self):
        filename = self.file_entry.get().strip()
        if not filename or not os.path.exists(filename):
            messagebox.showerror("File Error", "Please specify a valid file path to parse.")
            return

        self.output_textbox.delete("1.0", "end")
        self.valid_readings.clear()

        header_str = f"{'Timestamp':<20} | {'Sensor ID':<12} | {'Temp (°C)':<12} | {'Status'}\n"
        divider = "-" * 62 + "\n"
        self.output_textbox.insert("end", header_str)
        self.output_textbox.insert("end", divider)

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

                    if status != "OK" or raw_field == "INVALID":
                        self.output_textbox.insert(
                            "end",
                            f"{timestamp:<20} | {sensor_id:<12} | {'N/A':<12} | DISCARDED\n"
                        )
                        continue

                    unit = raw_field[-1].upper()
                    numeric_str = raw_field[:-1]

                    try:
                        raw_temp = float(numeric_str)
                        celsius = self.convert_to_celsius(raw_temp, unit)
                        if celsius is not None:
                            self.valid_readings.append(celsius)
                            self.output_textbox.insert(
                                "end",
                                f"{timestamp:<20} | {sensor_id:<12} | {celsius:<12.2f} | VALID\n"
                            )
                    except ValueError:
                        self.output_textbox.insert(
                            "end",
                            f"{timestamp:<20} | {sensor_id:<12} | {'ERROR':<12} | PARSE_FAILED\n"
                        )

            self.update_statistics()

        except Exception as e:
            messagebox.showerror("Execution Error", f"An error occurred while parsing:\n{str(e)}")

    def update_statistics(self):
        if self.valid_readings:
            avg_temp = sum(self.valid_readings) / len(self.valid_readings)
            min_temp = min(self.valid_readings)
            max_temp = max(self.valid_readings)

            self.stat_count.configure(text=str(len(self.valid_readings)))
            self.stat_avg.configure(text=f"{avg_temp:.2f} °C")
            self.stat_min.configure(text=f"{min_temp:.2f} °C")
            self.stat_max.configure(text=f"{max_temp:.2f} °C")
        else:
            self.stat_count.configure(text="0")
            self.stat_avg.configure(text="--")
            self.stat_min.configure(text="--")
            self.stat_max.configure(text="--")

if __name__ == "__main__":
    app = SensorParserApp()
    app.mainloop()
