import customtkinter as ctk
import os
import glob
import time
import threading

# ======================
# Keylogger Detector Logic (Text File Monitoring Only)
# ======================

class KeyloggerDetector:
    def __init__(self, gui_callback):
        self.running = False
        self.gui_callback = gui_callback
        self.files_state = {}  
    def start(self):
        self.running = True
        t = threading.Thread(target=self.monitor, daemon=True)
        t.start()

    def stop(self):
        self.running = False

    def monitor(self):
        while self.running:
            self.check_logs()
            time.sleep(5)

    def check_logs(self):
        current_dir = os.getcwd()
        for file in glob.glob(os.path.join(current_dir, "*.txt")):
            try:
                stat = os.stat(file)
                last_modified = stat.st_mtime
                size = stat.st_size

                if file not in self.files_state:
                    self.files_state[file] = (size, last_modified)
                else:
                    prev_size, prev_mtime = self.files_state[file]
                    if size != prev_size or last_modified != prev_mtime:
                        self.gui_callback(f"[ALERT] File modified: {file}")
                        self.files_state[file] = (size, last_modified)

            except FileNotFoundError:
                continue

# ======================
# GUI Application
# ======================

class DetectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Keylogger Detector (Text File Monitoring Only)")
        self.geometry("700x500")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.detector = KeyloggerDetector(self.add_alert)

        # Title
        self.label = ctk.CTkLabel(self, text="Keylogger Detector", font=("Arial", 20, "bold"))
        self.label.pack(pady=15)

        # Buttons
        self.start_button = ctk.CTkButton(self, text="Start Detection", command=self.start_detection, width=150, height=40)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop Detection", command=self.stop_detection, width=150, height=40)
        self.stop_button.pack(pady=10)

        # Status
        self.status_label = ctk.CTkLabel(self, text="Status: Stopped", font=("Arial", 14))
        self.status_label.pack(pady=10)

        # Alerts
        self.alerts_box = ctk.CTkTextbox(self, width=650, height=300, font=("Consolas", 12))
        self.alerts_box.pack(pady=10)

    def start_detection(self):
        self.detector.start()
        self.status_label.configure(text="Status: Monitoring...")

    def stop_detection(self):
        self.detector.stop()
        self.status_label.configure(text="Status: Stopped")

    def add_alert(self, msg):
        self.alerts_box.insert("end", msg + "\n")
        self.alerts_box.see("end")

# ======================
# Run App
# ======================

if __name__ == "__main__":
    app = DetectorApp()
    app.mainloop()
