import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pystray
from PIL import Image, ImageDraw

# logs
ARCHIVO_LOG = 'registro_eventos.txt'
logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class MonitorHandler(FileSystemEventHandler):
    """Manejo de eventos"""
    def __init__(self, log_widget):
        self.log_widget = log_widget

    def on_any_event(self, event):
        ruta_actual = os.path.normpath(event.src_path)
        nombre_archivo = os.path.basename(ruta_actual)
        evento = event.event_type.upper()
        tipo_elemento = "CARPETA" if event.is_directory else "ARCHIVO"

        # no toma en cuenta los archivos temporales
        if not event.is_directory:
            extensiones_basura = ('.tmp', '.crdownload', '.part', '.swp', '.log')
            prefijos_basura = ('~', '.$')
            if nombre_archivo.startswith(prefijos_basura) or nombre_archivo.endswith(extensiones_basura):
                return

        mensaje_ui = f"[{evento}] {tipo_elemento}: {ruta_actual}\n"
        self.actualizar_ui(mensaje_ui)
        logging.info(mensaje_ui.strip())

    def actualizar_ui(self, mensaje):
        self.log_widget.after(0, lambda: self.log_widget.insert(tk.END, mensaje))
        self.log_widget.after(0, self.log_widget.see, tk.END)


class DaemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Demonio de vigilancia de carpeta")
        self.root.geometry("600x450")
        self.observer = None
        self.tray_icon = None

        # Interceptar el botón "X" de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        # interfaz grafica
        self.frame_botones = tk.Frame(root)
        self.frame_botones.pack(pady=15)

        self.btn_select = tk.Button(self.frame_botones, text="▶ Iniciar Vigilancia", command=self.select_folder, bg="#d4edda")
        self.btn_select.grid(row=0, column=0, padx=10)

        self.btn_stop = tk.Button(self.frame_botones, text="⏹ Detener vigilancia", command=self.stop_monitoring, state=tk.DISABLED, bg="#f8d7da")
        self.btn_stop.grid(row=0, column=1, padx=10)

        self.btn_history = tk.Button(self.frame_botones, text="📄 Consultar Historial", command=self.show_history, bg="#cce5ff")
        self.btn_history.grid(row=0, column=2, padx=10)

        self.log_area = scrolledtext.ScrolledText(root, width=70, height=20)
        self.log_area.pack(padx=10, pady=5)
        self.log_area.insert(tk.END, "Esperando instrucciones...\n\n")

    # monitoreo
    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.start_monitoring(path)

    def start_monitoring(self, path):
        if self.observer:
            self.stop_monitoring()

        self.log_area.insert(tk.END, f"--- Iniciando vigilancia en: {path} ---\n")
        logging.info(f"INICIO DE MONITOREO: {path}")
        
        self.btn_select.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

        # instruccion por texto
        event_handler = MonitorHandler(self.log_area)
        self.observer = Observer()
        self.observer.schedule(event_handler, path, recursive=True)
        
        threading.Thread(target=self.observer.start, daemon=True).start()

    def stop_monitoring(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.log_area.insert(tk.END, "--- Vigilancia detenida ---\n\n")
            logging.info("VIGILANCIA DETENIDA")
            
            self.btn_select.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)

    def show_history(self):
        if not os.path.exists(ARCHIVO_LOG):
            messagebox.showinfo("Aún no hay un historial registrado")
            return

        try:
            if platform.system() == 'Windows':
                os.startfile(ARCHIVO_LOG)
            elif platform.system() == 'Darwin':
                subprocess.call(('open', ARCHIVO_LOG))
            else:
                subprocess.call(('xdg-open', ARCHIVO_LOG))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el historial:\n{e}")

    # --- LÓGICA DE LA BANDEJA DEL SISTEMA ---
    def hide_window(self):
        self.root.withdraw() 
        self.create_tray_icon()

    def create_tray_icon(self):
        image = Image.new('RGB', (64, 64), color=(0, 120, 215))
        d = ImageDraw.Draw(image)
        d.rectangle([16, 16, 48, 48], fill=(255, 255, 255))

        menu = pystray.Menu(
            pystray.MenuItem('Mostrar Interfaz', self.show_window),
            pystray.MenuItem('Cerrar por completo', self.quit_app)
        )

        self.tray_icon = pystray.Icon("MonitorDaemon", image, "Monitor de Carpetas", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self, icon, item):
        self.tray_icon.stop()
        self.root.after(0, self.root.deiconify)

    def quit_app(self, icon, item):
        self.tray_icon.stop()
        self.stop_monitoring()
        logging.info("APLICACIÓN CERRADA\n" + "-"*40)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = DaemonApp(root)
    root.mainloop()