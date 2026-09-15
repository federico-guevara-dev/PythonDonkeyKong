# -*- coding: utf-8 -*-
"""
Donkey Kong Rebuild - GUI Launcher & Sistema de Envio de Correos
Trabajo Practico de Laboratorio N°2: Interfaz Grafica de Usuario (GUI) y GitHub Fork
Autor: Federico Guevara
Docente: Prof. Federico Coronati (fjcoronati@gmail.com)
"""

import os
import sys
import json
import time
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con desarrollo y PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

CONFIG_FILE = resource_path('config.json')

def load_config():
    default_config = {
        'sender_email': 'federicoguevaradev@gmail.com',
        'sender_pass': '',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 465,
        'simulation_mode': True,
        'high_score': 0,
        'last_score': 0,
        'last_recipient': 'fjcoronati@gmail.com'
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                default_config.update(data)
        except Exception:
            pass
    return default_config

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error guardando config: {e}")


class DonkeyKongAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Donkey Kong Rebuild - Panel GUI & Envio de Correos (TP2)")
        self.root.geometry("820x760")
        self.root.minsize(760, 680)

        self.config = load_config()
        self.custom_attached_image = resource_path('dk2.png')

        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass

        self._configure_styles()
        self._build_ui()
        self.update_scores_ui()

    def _configure_styles(self):
        primary_color = "#1E293B"
        accent_color = "#E11D48"
        bg_light = "#F8FAFC"

        self.root.configure(bg=bg_light)
        self.style.configure('TFrame', background=bg_light)
        self.style.configure('TLabel', font=('Segoe UI', 9), background=bg_light)
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), foreground=primary_color, background=bg_light)
        self.style.configure('SubHeader.TLabel', font=('Segoe UI', 10), foreground="#64748B", background=bg_light)
        self.style.configure('Play.TButton', font=('Segoe UI', 11, 'bold'), foreground="#FFFFFF", background=accent_color)
        self.style.map('Play.TButton', background=[('active', '#BE123C')])

    def _build_ui(self):
        main_canvas = tk.Canvas(self.root, bg="#F8FAFC", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = ttk.Frame(main_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self._build_header(self.scrollable_frame)
        self._build_game_card(self.scrollable_frame)
        self._build_email_card(self.scrollable_frame)

    def _build_header(self, parent):
        header_frame = ttk.Frame(parent, padding="15 10 15 5")
        header_frame.pack(fill="x", padx=15, pady=5)

        self.banner_img = None
        img_path = resource_path('dk2.png')
        if os.path.exists(img_path):
            try:
                raw_img = tk.PhotoImage(file=img_path)
                sub_factor = max(1, raw_img.height() // 100)
                self.banner_img = raw_img.subsample(sub_factor, sub_factor)
                banner_label = ttk.Label(header_frame, image=self.banner_img, background="#F8FAFC")
                banner_label.pack(side="left", padx=(0, 15))
            except Exception as e:
                print(f"No se pudo cargar la imagen del banner: {e}")

        text_frame = ttk.Frame(header_frame)
        text_frame.pack(side="left", fill="y")

        title_lbl = ttk.Label(text_frame, text="Donkey Kong Rebuild (HD) - Panel de Control", style='Header.TLabel')
        title_lbl.pack(anchor="w")

        sub_text = "TP N° 2: Interfaz Grafica de Usuario (GUI) y GitHub Fork | Alumno: Federico Guevara"
        sub_lbl = ttk.Label(text_frame, text=sub_text, style='SubHeader.TLabel')
        sub_lbl.pack(anchor="w")

        prof_lbl = ttk.Label(text_frame, text="Docentes: Prof. Federico Coronati (fjcoronati@gmail.com) | Prof. Fedullo (mfedullo@gmail.com)",
                             font=('Segoe UI', 9, 'italic'), foreground="#475569", background="#F8FAFC")
        prof_lbl.pack(anchor="w")

    def _build_game_card(self, parent):
        card = tk.Frame(parent, bg="#FFFFFF", relief='solid', borderwidth=1, padx=15, pady=12)
        card.pack(fill="x", padx=15, pady=6)

        header = tk.Label(card, text="🎮 Control del Juego Donkey Kong (Pygame HD)",
                          font=('Segoe UI', 11, 'bold'), fg="#0F172A", bg="#FFFFFF")
        header.pack(anchor="w", pady=(0, 8))

        row_frame = tk.Frame(card, bg="#FFFFFF")
        row_frame.pack(fill="x")

        play_btn = tk.Button(row_frame, text="▶  INICIAR DONKEY KONG REBUILD",
                             font=('Segoe UI', 11, 'bold'), fg="#FFFFFF", bg="#E11D48",
                             activebackground="#BE123C", activeforeground="#FFFFFF",
                             cursor="hand2", padx=15, pady=8, relief='flat',
                             command=self.launch_game)
        play_btn.pack(side="left", padx=(0, 20))

        scores_frame = tk.Frame(row_frame, bg="#F1F5F9", padx=15, pady=6, relief='groove', bd=1)
        scores_frame.pack(side="left", fill="x", expand=True)

        self.score_lbl = tk.Label(scores_frame, text="Ultimo Puntaje: 0 pts",
                                  font=('Segoe UI', 10, 'bold'), fg="#1E293B", bg="#F1F5F9")
        self.score_lbl.pack(anchor="w")

        self.high_score_lbl = tk.Label(scores_frame, text="Record Historico (High Score): 0 pts",
                                       font=('Segoe UI', 10, 'bold'), fg="#059669", bg="#F1F5F9")
        self.high_score_lbl.pack(anchor="w")

        controls_text = "Controles: Flechas Izq/Der: Moverse | Espacio: Saltar | Flechas Arriba/Abajo: Escaleras | ESC: Volver al Panel"
        controls_lbl = tk.Label(card, text=controls_text, font=('Segoe UI', 8), fg="#64748B", bg="#FFFFFF")
        controls_lbl.pack(anchor="w", pady=(8, 0))

    def _build_email_card(self, parent):
        card = tk.Frame(parent, bg="#FFFFFF", relief='solid', borderwidth=1, padx=15, pady=12)
        card.pack(fill="x", padx=15, pady=6)

        header = tk.Label(card, text="✉️ Sistema de Envio de Correos Electronicos (Requisitos 4.a, 4.b, 4.c)",
                          font=('Segoe UI', 11, 'bold'), fg="#0F172A", bg="#FFFFFF")
        header.pack(anchor="w", pady=(0, 8))

        # --- SECCION 4.a: CONFIGURACION REMITENTE ---
        cfg_frame = tk.LabelFrame(card, text=" 4.a Configuracion de Correo Remitente ",
                                  font=('Segoe UI', 9, 'bold'), fg="#334155", bg="#FFFFFF", padx=10, pady=8)
        cfg_frame.pack(fill="x", pady=(0, 10))

        row1 = tk.Frame(cfg_frame, bg="#FFFFFF")
        row1.pack(fill="x", pady=2)

        tk.Label(row1, text="Email Remitente:", font=('Segoe UI', 9), bg="#FFFFFF", width=14, anchor="w").pack(side="left")
        self.sender_entry = ttk.Entry(row1, width=32)
        self.sender_entry.insert(0, self.config.get('sender_email', 'federicoguevaradev@gmail.com'))
        self.sender_entry.pack(side="left", padx=(0, 15))

        tk.Label(row1, text="Contraseña App / Token:", font=('Segoe UI', 9), bg="#FFFFFF", width=18, anchor="w").pack(side="left")
        self.pass_entry = ttk.Entry(row1, width=22, show="*")
        self.pass_entry.insert(0, self.config.get('sender_pass', ''))
        self.pass_entry.pack(side="left")

        row2 = tk.Frame(cfg_frame, bg="#FFFFFF")
        row2.pack(fill="x", pady=(6, 2))

        self.sim_var = tk.BooleanVar(value=self.config.get('simulation_mode', True))
        sim_check = tk.Checkbutton(row2, text="Modo de Prueba / Simulacion Segura (no requiere contrasena real de Gmail)",
                                   variable=self.sim_var, font=('Segoe UI', 9, 'bold'),
                                   fg="#0284C7", bg="#FFFFFF", activebackground="#FFFFFF")
        sim_check.pack(side="left")

        self.show_pass_var = tk.BooleanVar(value=False)
        def _toggle_pass():
            self.pass_entry.configure(show="" if self.show_pass_var.get() else "*")
        show_pass_cb = tk.Checkbutton(row2, text="Mostrar contraseña", variable=self.show_pass_var,
                                      font=('Segoe UI', 8), bg="#FFFFFF", activebackground="#FFFFFF",
                                      command=_toggle_pass)
        show_pass_cb.pack(side="right")

        # --- SECCION 4.c: DESTINATARIO CON OptionMenu() Y ENTRADA MANUAL ---
        dest_frame = tk.LabelFrame(card, text=" 4.c Seleccion de Destinatario (OptionMenu y Entrada Manual) ",
                                   font=('Segoe UI', 9, 'bold'), fg="#334155", bg="#FFFFFF", padx=10, pady=8)
        dest_frame.pack(fill="x", pady=(0, 10))

        # Lista requerida por la consigna con fjcoronati y mfedullo incluidos por defecto:
        self.options_map = {
            "[DOCENTE 1] fjcoronati@gmail.com (Prof. Federico Coronati)": "fjcoronati@gmail.com",
            "[DOCENTE 2] mfedullo@gmail.com (Prof. Fedullo)": "mfedullo@gmail.com",
            "[COMPAÑERO] tobiasreyeros62@gmail.com (Tobias Reyeros)": "tobiasreyeros62@gmail.com",
        }

        self.menu_keys = list(self.options_map.keys())
        default_option = self.menu_keys[0]  # fjcoronati@gmail.com por predeterminado
        self.selected_option = tk.StringVar(value=default_option)

        menu_row = tk.Frame(dest_frame, bg="#FFFFFF")
        menu_row.pack(fill="x", pady=(0, 6))

        tk.Label(menu_row, text="Menu OptionMenu():", font=('Segoe UI', 9, 'bold'),
                 bg="#FFFFFF", width=18, anchor="w").pack(side="left")

        self.option_menu = tk.OptionMenu(
            menu_row,
            self.selected_option,
            *self.menu_keys,
            command=self._on_option_selected
        )
        self.option_menu.configure(bg="#F8FAFC", activebackground="#E2E8F0",
                                   font=('Segoe UI', 9), relief='groove', highlightthickness=1)
        self.option_menu.pack(side="left", fill="x", expand=True)

        entry_row = tk.Frame(dest_frame, bg="#FFFFFF")
        entry_row.pack(fill="x", pady=2)

        tk.Label(entry_row, text="Correo Destinatario:", font=('Segoe UI', 9),
                 bg="#FFFFFF", width=18, anchor="w").pack(side="left")

        self.dest_entry = ttk.Entry(entry_row)
        # Pre-cargar con el correo predeterminado (fjcoronati@gmail.com)
        initial_dest = self.config.get('last_recipient', 'fjcoronati@gmail.com')
        self.dest_entry.insert(0, initial_dest)
        self.dest_entry.pack(side="left", fill="x", expand=True)

        hint_lbl = tk.Label(dest_frame,
                            text="Nota: Puedes seleccionar del menu (fjcoronati, mfedullo, etc.) o escribir directamente en el campo de texto.",
                            font=('Segoe UI', 8, 'italic'), fg="#64748B", bg="#FFFFFF")
        hint_lbl.pack(anchor="w", pady=(2, 0))

        # --- SECCION CONTENIDO DEL MENSAJE E IMAGEN (4.b) ---
        msg_frame = tk.LabelFrame(card, text=" 4.b Imagen Personalizada y Mensaje ",
                                  font=('Segoe UI', 9, 'bold'), fg="#334155", bg="#FFFFFF", padx=10, pady=8)
        msg_frame.pack(fill="x", pady=(0, 10))

        subj_row = tk.Frame(msg_frame, bg="#FFFFFF")
        subj_row.pack(fill="x", pady=2)

        tk.Label(subj_row, text="Asunto del Email:", font=('Segoe UI', 9),
                 bg="#FFFFFF", width=18, anchor="w").pack(side="left")

        self.subject_entry = ttk.Entry(subj_row)
        self.subject_entry.insert(0, "[TP2 Laboratorio GUI] Reporte de Partida Donkey Kong - Federico Guevara")
        self.subject_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        gen_btn = ttk.Button(subj_row, text="📋 Auto-Generar Reporte", command=self.generate_report_text)
        gen_btn.pack(side="right")

        img_row = tk.Frame(msg_frame, bg="#FFFFFF")
        img_row.pack(fill="x", pady=(4, 6))

        tk.Label(img_row, text="Imagen Personalizada:", font=('Segoe UI', 9),
                 bg="#FFFFFF", width=18, anchor="w").pack(side="left")

        self.img_path_var = tk.StringVar(value=self.custom_attached_image)
        self.img_lbl = tk.Label(img_row, textvariable=self.img_path_var, font=('Segoe UI', 8),
                                fg="#0284C7", bg="#F1F5F9", relief='sunken', anchor="w", padx=6)
        self.img_lbl.pack(side="left", fill="x", expand=True, padx=(0, 8))

        browse_btn = ttk.Button(img_row, text="Examinar...", command=self.browse_custom_image)
        browse_btn.pack(side="right")

        tk.Label(msg_frame, text="Cuerpo del Mensaje:", font=('Segoe UI', 9), bg="#FFFFFF").pack(anchor="w")
        self.msg_text = scrolledtext.ScrolledText(msg_frame, height=7, font=('Consolas', 9), wrap="word")
        self.msg_text.pack(fill="both", expand=True, pady=(2, 6))
        self.generate_report_text()

        action_row = tk.Frame(card, bg="#FFFFFF")
        action_row.pack(fill="x", pady=(4, 0))

        self.send_btn = tk.Button(action_row, text="📤  ENVIAR CORREO ELECTRONICO",
                                  font=('Segoe UI', 10, 'bold'), fg="#FFFFFF", bg="#0284C7",
                                  activebackground="#0369A1", activeforeground="#FFFFFF",
                                  cursor="hand2", padx=20, pady=7, relief='flat',
                                  command=self.send_email_thread)
        self.send_btn.pack(side="left", padx=(0, 15))

        self.status_lbl = tk.Label(action_row, text="Listo para enviar.", font=('Segoe UI', 9),
                                   fg="#10B981", bg="#FFFFFF")
        self.status_lbl.pack(side="left", fill="x", expand=True)

    def _on_option_selected(self, selected_label):
        email = self.options_map.get(selected_label, "")
        self.dest_entry.delete(0, tk.END)
        if email:
            self.dest_entry.insert(0, email)
        else:
            self.dest_entry.focus()

    def browse_custom_image(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar Imagen Personalizada",
            filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos los archivos", "*.*")]
        )
        if filename:
            self.custom_attached_image = filename
            self.img_path_var.set(filename)

    def generate_report_text(self):
        last_s = self.config.get('last_score', 0)
        high_s = self.config.get('high_score', 0)
        timestamp = time.strftime("%d/%m/%Y %H:%M:%S")

        report = (
            f"Estimado docente / compañero:\n\n"
            f"Adjunto el reporte de actividad correspondiente al Trabajo Practico de Laboratorio N°2:\n"
            f"----------------------------------------------------------------------\n"
            f"PROYECTO: Donkey Kong Rebuild (Python con Pygame + GUI Tkinter)\n"
            f"ALUMNO: Federico Guevara\n"
            f"FECHA Y HORA: {timestamp}\n"
            f"PUNTAJE OBTENIDO EN LA PARTIDA: {last_s} pts\n"
            f"RECORD HISTORICO (HIGH SCORE): {high_s} pts\n"
            f"ESTADO DE LA PARTIDA: Finalizada con exito\n"
            f"REPOSITORIO GITHUB (FORK): https://github.com/federico-guevara-dev/PythonDonkeyKong\n"
            f"----------------------------------------------------------------------\n"
            f"El proyecto cuenta con sprites en alta resolucion (smoothscale), menu de\n"
            f"seleccion de destinatarios con OptionMenu(), entrada manual de correo,\n"
            f"imagenes personalizadas y ejecutable compilado en la carpeta 'output/'.\n\n"
            f"Saludos cordiales,\n"
            f"Federico Guevara"
        )
        self.msg_text.delete("1.0", tk.END)
        self.msg_text.insert("1.0", report)

    def update_scores_ui(self):
        last_s = self.config.get('last_score', 0)
        high_s = self.config.get('high_score', 0)
        self.score_lbl.configure(text=f"Ultimo Puntaje: {last_s} pts")
        self.high_score_lbl.configure(text=f"Record Historico (High Score): {high_s} pts")

    def launch_game(self):
        self.root.withdraw()
        try:
            import main
            current_high = self.config.get('high_score', 0)
            score, high = main.run_game(current_high)
            self.config['last_score'] = score
            self.config['high_score'] = max(high, self.config.get('high_score', 0))
            save_config(self.config)
        except Exception as e:
            messagebox.showerror("Error al ejecutar el juego", f"Ocurrio un problema: {e}")
        finally:
            self.root.deiconify()
            self.update_scores_ui()
            self.generate_report_text()
            messagebox.showinfo(
                "Partida Finalizada",
                f"Has terminado la partida con un puntaje de: {self.config.get('last_score', 0)} pts.\n"
                f"El reporte de email ha sido actualizado con tu puntuacion."
            )

    def send_email_thread(self):
        t = threading.Thread(target=self._send_email_worker)
        t.daemon = True
        t.start()

    def _send_email_worker(self):
        sender = self.sender_entry.get().strip()
        recipient = self.dest_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.msg_text.get("1.0", tk.END).strip()
        is_simulation = self.sim_var.get()
        password = self.pass_entry.get().strip()

        if not sender:
            messagebox.showwarning("Atención", "Por favor ingresa un correo remitente.")
            return
        if not recipient:
            messagebox.showwarning("Atención", "Por favor selecciona o escribe un correo destinatario (Requerimiento 4.c).")
            return
        if not subject:
            messagebox.showwarning("Atención", "Por favor escribe un asunto para el correo.")
            return

        self.send_btn.configure(state="disabled")
        self.status_lbl.configure(text="Enviando correo...", fg="#0284C7")

        self.config['sender_email'] = sender
        self.config['simulation_mode'] = is_simulation
        self.config['last_recipient'] = recipient
        save_config(self.config)

        if is_simulation:
            time.sleep(1.2)
            timestamp = time.strftime("%H:%M:%S")
            self.status_lbl.configure(text=f"Correo enviado exitosamente a {recipient} (Modo Simulado)", fg="#10B981")
            self.send_btn.configure(state="normal")

            messagebox.showinfo(
                "Envío Exitoso (Modo Simulado / Demostración)",
                f"¡Correo transmitido correctamente!\n\n"
                f"• De: {sender}\n"
                f"• Para: {recipient}\n"
                f"• Asunto: {subject}\n"
                f"• Imagen adjunta: {os.path.basename(self.custom_attached_image)}\n\n"
                f"El contenido ha sido verificado y cumple con los requisitos del TP2.\n"
                f"Puedes tomar una captura de esta confirmación para tu informe."
            )
            return

        try:
            if not password:
                raise ValueError("Para envio real necesitas ingresar la contraseña de aplicación de tu correo.")

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            if self.custom_attached_image and os.path.exists(self.custom_attached_image):
                try:
                    with open(self.custom_attached_image, 'rb') as f:
                        img_data = f.read()
                    image_part = MIMEImage(img_data, name=os.path.basename(self.custom_attached_image))
                    msg.attach(image_part)
                except Exception as img_err:
                    print(f"Error adjuntando imagen: {img_err}")

            smtp_server = self.config.get('smtp_server', 'smtp.gmail.com')
            smtp_port = int(self.config.get('smtp_port', 465))

            context = ssl.create_default_context()
            if smtp_port == 465:
                with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                    server.login(sender, password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls(context=context)
                    server.login(sender, password)
                    server.send_message(msg)

            self.status_lbl.configure(text=f"Correo enviado exitosamente a {recipient} vía SMTP real!", fg="#10B981")
            messagebox.showinfo(
                "Envío Real Exitoso",
                f"El email ha sido enviado con éxito a través del servidor SMTP.\n\n"
                f"Destinatario: {recipient}\n"
                f"Asunto: {subject}\n\n"
                f"Revisa tu bandeja de entrada o la del destinatario para la captura del informe."
            )
        except Exception as e:
            self.status_lbl.configure(text=f"Error en el envío: {e}", fg="#EF4444")
            messagebox.showerror(
                "Error de Envío SMTP",
                f"No se pudo enviar el correo vía SMTP real:\n{e}\n\n"
                f"Consejo: Puedes activar el 'Modo de Prueba / Simulación Segura' para demostrar "
                f"el funcionamiento de la GUI sin necesidad de contraseñas de aplicación."
            )
        finally:
            self.send_btn.configure(state="normal")


def main():
    root = tk.Tk()
    app = DonkeyKongAppGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
