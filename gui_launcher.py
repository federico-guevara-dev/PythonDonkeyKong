# -*- coding: utf-8 -*-
"""Donkey Kong Rebuild - GUI Launcher & Envio de Correos (TP2)
Autor: Federico Guevara | Docente: Prof. Federico Coronati"""

import os,sys,json,time,smtplib,ssl,threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import tkinter as tk
from tkinter import ttk,messagebox,scrolledtext,filedialog

# Variables de entorno para credenciales
EMAIL_REMITENTE=os.environ.get("DK_EMAIL","elcrack35158@gmail.com")
EMAIL_PASSWORD=os.environ.get("DK_EMAIL_PASS","")
SMTP_SERVER=os.environ.get("DK_SMTP_SERVER","smtp.gmail.com")
SMTP_PORT=int(os.environ.get("DK_SMTP_PORT","465"))
ALUMNO=os.environ.get("DK_ALUMNO","Federico Guevara")
REPO_URL=os.environ.get("DK_REPO","https://github.com/federico-guevara-dev/PythonDonkeyKong")

def resource_path(p):
    try: base=sys._MEIPASS
    except: base=os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base,p)

CONFIG_FILE=resource_path("config.json")

def load_config():
    cfg={"high_score":0,"last_score":0,"last_recipient":"fjcoronati@gmail.com","simulation_mode":True}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE,"r",encoding="utf-8") as f: cfg.update(json.load(f))
        except: pass
    return cfg

def save_config(cfg):
    try:
        with open(CONFIG_FILE,"w",encoding="utf-8") as f: json.dump(cfg,f,indent=2)
    except: pass


class App:
    def __init__(self,root):
        self.root=root
        self.root.title("Donkey Kong Rebuild - Panel GUI (TP2)")
        self.root.geometry("780x620")
        self.root.configure(bg="#1a1a2e")
        self.cfg=load_config()
        self.img_adjunta=resource_path("dk2.png")
        self._build()
        self._update_scores()

    def _build(self):
        bg="#1a1a2e"
        fg="#eee"
        card_bg="#16213e"
        accent="#e94560"

        # Titulo
        tk.Label(self.root,text="🦍 Donkey Kong Rebuild",font=("Segoe UI",18,"bold"),
                 fg=accent,bg=bg).pack(pady=(12,2))
        tk.Label(self.root,text=f"TP2 - {ALUMNO}",font=("Segoe UI",10),
                 fg="#888",bg=bg).pack()

        # Juego
        game=tk.Frame(self.root,bg=card_bg,padx=12,pady=10)
        game.pack(fill="x",padx=15,pady=8)

        row=tk.Frame(game,bg=card_bg)
        row.pack(fill="x")

        tk.Button(row,text="▶ JUGAR",font=("Segoe UI",12,"bold"),fg="#fff",bg=accent,
                  activebackground="#c81e45",relief="flat",padx=20,pady=6,cursor="hand2",
                  command=self._play).pack(side="left")

        sf=tk.Frame(row,bg="#0f3460",padx=10,pady=4)
        sf.pack(side="left",fill="x",expand=True,padx=(12,0))
        self.lbl_score=tk.Label(sf,text="Puntaje: 0",font=("Segoe UI",10,"bold"),fg=fg,bg="#0f3460")
        self.lbl_score.pack(anchor="w")
        self.lbl_high=tk.Label(sf,text="Record: 0",font=("Segoe UI",10,"bold"),fg="#0f9b58",bg="#0f3460")
        self.lbl_high.pack(anchor="w")

        tk.Label(game,text="← → Moverse | Espacio: Saltar | ↑↓ Escaleras | ESC: Salir",
                 font=("Segoe UI",8),fg="#666",bg=card_bg).pack(anchor="w",pady=(6,0))

        # Email
        email=tk.Frame(self.root,bg=card_bg,padx=12,pady=10)
        email.pack(fill="x",padx=15,pady=4)

        tk.Label(email,text="✉ Envio de Correo",font=("Segoe UI",12,"bold"),
                 fg=fg,bg=card_bg).pack(anchor="w",pady=(0,6))

        # Remitente (desde variable de entorno)
        r1=tk.Frame(email,bg=card_bg)
        r1.pack(fill="x",pady=2)
        tk.Label(r1,text="De:",font=("Segoe UI",9),fg=fg,bg=card_bg,width=10,anchor="w").pack(side="left")
        self.ent_from=ttk.Entry(r1,width=30)
        self.ent_from.insert(0,EMAIL_REMITENTE)
        self.ent_from.pack(side="left",padx=(0,10))
        tk.Label(r1,text="Pass:",font=("Segoe UI",9),fg=fg,bg=card_bg).pack(side="left")
        self.ent_pass=ttk.Entry(r1,width=20,show="*")
        self.ent_pass.insert(0,EMAIL_PASSWORD)
        self.ent_pass.pack(side="left")

        # Simulacion
        r1b=tk.Frame(email,bg=card_bg)
        r1b.pack(fill="x",pady=2)
        self.sim_var=tk.BooleanVar(value=self.cfg.get("simulation_mode",True))
        tk.Checkbutton(r1b,text="Modo simulado (no requiere password real)",
                       variable=self.sim_var,font=("Segoe UI",9),fg="#4fc3f7",bg=card_bg,
                       selectcolor=card_bg,activebackground=card_bg).pack(side="left")

        # Destinatario con OptionMenu
        r2=tk.Frame(email,bg=card_bg)
        r2.pack(fill="x",pady=2)
        tk.Label(r2,text="Para:",font=("Segoe UI",9),fg=fg,bg=card_bg,width=10,anchor="w").pack(side="left")

        self.opciones={
            "fjcoronati@gmail.com (Prof. Coronati)":"fjcoronati@gmail.com",
            "mfedullo@gmail.com (Prof. Fedullo)":"mfedullo@gmail.com",
            "tobiasreyeros62@gmail.com (Tobias)":"tobiasreyeros62@gmail.com",
        }
        keys=list(self.opciones.keys())
        self.sel_opt=tk.StringVar(value=keys[0])
        tk.OptionMenu(r2,self.sel_opt,*keys,command=self._on_select).pack(side="left",padx=(0,8))

        self.ent_to=ttk.Entry(r2)
        self.ent_to.insert(0,self.cfg.get("last_recipient","fjcoronati@gmail.com"))
        self.ent_to.pack(side="left",fill="x",expand=True)

        # Asunto
        r3=tk.Frame(email,bg=card_bg)
        r3.pack(fill="x",pady=2)
        tk.Label(r3,text="Asunto:",font=("Segoe UI",9),fg=fg,bg=card_bg,width=10,anchor="w").pack(side="left")
        self.ent_subj=ttk.Entry(r3)
        self.ent_subj.insert(0,f"[TP2] Reporte Donkey Kong - {ALUMNO}")
        self.ent_subj.pack(side="left",fill="x",expand=True)

        # Imagen
        r4=tk.Frame(email,bg=card_bg)
        r4.pack(fill="x",pady=2)
        tk.Label(r4,text="Imagen:",font=("Segoe UI",9),fg=fg,bg=card_bg,width=10,anchor="w").pack(side="left")
        self.img_var=tk.StringVar(value=self.img_adjunta)
        tk.Label(r4,textvariable=self.img_var,font=("Segoe UI",8),fg="#4fc3f7",bg="#0f3460",
                 anchor="w",padx=4).pack(side="left",fill="x",expand=True,padx=(0,6))
        ttk.Button(r4,text="...",width=3,command=self._browse).pack(side="right")

        # Mensaje
        tk.Label(email,text="Mensaje:",font=("Segoe UI",9),fg=fg,bg=card_bg).pack(anchor="w",pady=(4,0))
        self.txt_msg=scrolledtext.ScrolledText(email,height=5,font=("Consolas",9),wrap="word")
        self.txt_msg.pack(fill="both",expand=True,pady=(2,6))
        self._gen_reporte()

        # Boton enviar
        r5=tk.Frame(email,bg=card_bg)
        r5.pack(fill="x")
        tk.Button(r5,text="📤 ENVIAR",font=("Segoe UI",10,"bold"),fg="#fff",bg="#0284c7",
                  activebackground="#026aa7",relief="flat",padx=16,pady=5,cursor="hand2",
                  command=self._send_thread).pack(side="left")
        self.lbl_status=tk.Label(r5,text="Listo",font=("Segoe UI",9),fg="#0f9b58",bg=card_bg)
        self.lbl_status.pack(side="left",padx=10)

    def _on_select(self,sel):
        email=self.opciones.get(sel,"")
        self.ent_to.delete(0,tk.END)
        if email: self.ent_to.insert(0,email)

    def _browse(self):
        f=filedialog.askopenfilename(filetypes=[("Imagenes","*.png *.jpg *.jpeg *.gif *.bmp")])
        if f:
            self.img_adjunta=f
            self.img_var.set(f)

    def _gen_reporte(self):
        s=self.cfg.get("last_score",0)
        h=self.cfg.get("high_score",0)
        t=time.strftime("%d/%m/%Y %H:%M:%S")
        txt=(f"Reporte TP2 - Donkey Kong Rebuild\n"
             f"Alumno: {ALUMNO}\n"
             f"Fecha: {t}\n"
             f"Puntaje: {s} pts | Record: {h} pts\n"
             f"Repo: {REPO_URL}\n\n"
             f"Saludos,\n{ALUMNO}")
        self.txt_msg.delete("1.0",tk.END)
        self.txt_msg.insert("1.0",txt)

    def _update_scores(self):
        self.lbl_score.configure(text=f"Puntaje: {self.cfg.get('last_score',0)}")
        self.lbl_high.configure(text=f"Record: {self.cfg.get('high_score',0)}")

    def _play(self):
        self.root.withdraw()
        try:
            import main
            score,high=main.run_game(self.cfg.get("high_score",0))
            self.cfg["last_score"]=score
            self.cfg["high_score"]=max(high,self.cfg.get("high_score",0))
            save_config(self.cfg)
        except Exception as e:
            messagebox.showerror("Error",str(e))
        finally:
            self.root.deiconify()
            self._update_scores()
            self._gen_reporte()

    def _send_thread(self):
        t=threading.Thread(target=self._send,daemon=True)
        t.start()

    def _send(self):
        sender=self.ent_from.get().strip()
        to=self.ent_to.get().strip()
        subj=self.ent_subj.get().strip()
        body=self.txt_msg.get("1.0",tk.END).strip()
        passw=self.ent_pass.get().strip()
        sim=self.sim_var.get()

        if not sender or not to or not subj:
            messagebox.showwarning("Faltan datos","Completa remitente, destinatario y asunto.")
            return

        self.lbl_status.configure(text="Enviando...",fg="#4fc3f7")
        self.cfg["last_recipient"]=to
        self.cfg["simulation_mode"]=sim
        save_config(self.cfg)

        if sim:
            time.sleep(0.8)
            self.lbl_status.configure(text=f"Enviado a {to} (simulado)",fg="#0f9b58")
            messagebox.showinfo("Enviado (Simulado)",
                f"De: {sender}\nPara: {to}\nAsunto: {subj}")
            return

        try:
            if not passw:
                raise ValueError("Necesitas password de app para envio real.")

            msg=MIMEMultipart()
            msg["From"]=sender
            msg["To"]=to
            msg["Subject"]=subj
            msg.attach(MIMEText(body,"plain","utf-8"))

            if self.img_adjunta and os.path.exists(self.img_adjunta):
                with open(self.img_adjunta,"rb") as f:
                    msg.attach(MIMEImage(f.read(),name=os.path.basename(self.img_adjunta)))

            ctx=ssl.create_default_context()
            port=SMTP_PORT
            if port==465:
                with smtplib.SMTP_SSL(SMTP_SERVER,port,context=ctx) as s:
                    s.login(sender,passw)
                    s.send_message(msg)
            else:
                with smtplib.SMTP(SMTP_SERVER,port) as s:
                    s.starttls(context=ctx)
                    s.login(sender,passw)
                    s.send_message(msg)

            self.lbl_status.configure(text=f"Enviado a {to}",fg="#0f9b58")
            messagebox.showinfo("Enviado",f"Correo enviado a {to}")
        except Exception as e:
            self.lbl_status.configure(text=f"Error: {e}",fg="#e94560")
            messagebox.showerror("Error",str(e))


def main():
    root=tk.Tk()
    App(root)
    root.mainloop()

if __name__=="__main__":
    main()
