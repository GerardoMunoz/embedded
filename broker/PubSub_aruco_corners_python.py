#!/usr/bin/env python3
"""
Pub/Sub TCP Client con GUI (para probar PubSub_server.py)
---------------------------------------------------------
Permite:
- Conectarse al broker TCP (por defecto localhost:5051)
- Suscribirse a tópicos
- Publicar mensajes JSON
- Ver los mensajes recibidos
- Ejecutar pruebas automáticas con payloads válidos de topics.md
- (extendido) Detectar ArUco, construir homografía y publicar pose de robots

Autor: ChatGPT + ajustes del usuario
"""

import socket
import threading
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import cv2
import numpy as np
from PIL import Image, ImageTk
import math

# ---------------------------
# Configuración de referencia / robots
# ---------------------------

# Tags de referencia 0..8 en un grid 3x3 (puedes ajustar distancias)
#   6  7  8   -> y = 2
#   3  4  5   -> y = 1
#   0  1  2   -> y = 0
REF_TAG_IDS = list(range(9))
REF_TAG_WORLD = {
    0: (0.0, 0.0),
    1: (1.0, 0.0),
    2: (2.0, 0.0),
    3: (0.0, 1.0),
    4: (1.0, 1.0),
    5: (2.0, 1.0),
    6: (0.0, 2.0),
    7: (1.0, 2.0),
    8: (2.0, 2.0),
}

# Robots: robot i -> tags 30+i y 40+i
MAX_ROBOTS = 10
ROBOT_TAGS = {
    i: [30 + i, 40 + i]
    for i in range(MAX_ROBOTS)
}

# ---------------------------
# Funciones auxiliares para ArUco / homografía / pose
# ---------------------------

def compute_tag_centers(ids, corners):
    """
    Convierte esquinas en centros.
    ids: array (N,) de ints
    corners: lista de N arrays (4,2)
    Devuelve dict: {id: (u,v)} en coordenadas de imagen.
    """
    centers = {}
    for tag_id, c in zip(ids, corners):
        c = c.reshape(-1, 2)
        u = float(np.mean(c[:, 0]))
        v = float(np.mean(c[:, 1]))
        centers[int(tag_id)] = (u, v)
    return centers


def compute_homography_from_refs(tag_centers_img, min_points=4):
    """
    Construye la homografía H (imagen -> mundo) usando SOLO tags de referencia.
    tag_centers_img: dict {id: (u,v)} en pixeles.
    Devuelve:
      - H (3x3) o None si no hay suficientes puntos.
    """
    pts_img = []
    pts_world = []

    for tag_id in REF_TAG_IDS:
        if tag_id in tag_centers_img:
            u, v = tag_centers_img[tag_id]
            xw, yw = REF_TAG_WORLD[tag_id]
            pts_img.append([u, v])
            pts_world.append([xw, yw])

    if len(pts_img) < min_points:
        return None

    pts_img = np.array(pts_img, dtype=np.float32)
    pts_world = np.array(pts_world, dtype=np.float32)

    H, mask = cv2.findHomography(pts_img, pts_world, cv2.RANSAC, ransacReprojThreshold=3.0)
    return H


def image_to_world(H, u, v):
    """
    Aplica la homografía H (imagen->mundo) a un punto (u,v) de la imagen.
    Devuelve (x,y) en coordenadas del mundo.
    """
    pt = np.array([u, v, 1.0], dtype=np.float64)
    warped = H @ pt
    if warped[2] == 0:
        return None
    x = warped[0] / warped[2]
    y = warped[1] / warped[2]
    return (float(x), float(y))


def project_all_tags_to_world(H, tag_centers_img):
    """
    Proyecta todos los tags detectados a coordenadas del mundo.
    Devuelve dict {id: (x,y)}.
    """
    world = {}
    for tag_id, (u, v) in tag_centers_img.items():
        p = image_to_world(H, u, v)
        if p is not None:
            world[tag_id] = p
    return world


def estimate_robot_pose(robot_id, tag_world_positions):
    """
    Calcula la pose (x, y, theta) del robot dado su ID.

    robot_id: entero (0..MAX_ROBOTS-1)
    tag_world_positions: dict {tag_id: (x,y)} con tags ya proyectados al mundo.

    Devuelve:
      - (x, y, theta_en_radianes) o None si no hay suficientes tags.
        theta puede ser None si solo se ve 1 tag.
    """
    if robot_id not in ROBOT_TAGS:
        return None

    tag_ids = ROBOT_TAGS[robot_id]
    present_tags = [tid for tid in tag_ids if tid in tag_world_positions]

    if len(present_tags) == 0:
        return None
    elif len(present_tags) == 1:
        tid = present_tags[0]
        x, y = tag_world_positions[tid]
        theta = None
        return (x, y, theta)
    else:
        tid1, tid2 = present_tags[:2]
        x1, y1 = tag_world_positions[tid1]
        x2, y2 = tag_world_positions[tid2]
        cx = 0.5 * (x1 + x2)
        cy = 0.5 * (y1 + y2)
        vx = x2 - x1
        vy = y2 - y1
        theta = math.atan2(vy, vx)
        return (cx, cy, theta)


# ---------------------------
# Hilo de cámara + ArUco + PubSub
# ---------------------------

class CameraThread(threading.Thread):
    def __init__(self, gui):
        super().__init__(daemon=True)
        self.gui = gui
        self.running = True
        self.latest_frame = None
        self.cap = cv2.VideoCapture(1)

        # Cargar ArUco
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)

        # Rango de IDs válidos (puedes ajustar)
        self.id_min = 0
        self.id_max = 50

        # Homografía actual (imagen -> mundo)
        self.H = None

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Detectar ArUco
            corners, ids, _ = self.detector.detectMarkers(frame)

            tag_centers_img = {}
            if ids is not None:
                ids_flat = ids.flatten()
                # Calcular centros
                tag_centers_img = compute_tag_centers(ids_flat, corners)

                # Actualizar homografía usando referencias (0..8)
                H_candidate = compute_homography_from_refs(tag_centers_img)
                if H_candidate is not None:
                    self.H = H_candidate

                # Dibujar markers
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)

                # Publicar corners crudos (opcional; puedes comentar si ya no lo quieres)
                for i, c in zip(ids_flat, corners):
                    if self.id_min <= int(i) <= self.id_max:
                        corner_list = c.reshape((-1, 2)).tolist()
                        pkt = {
                            "action": "PUB",
                            "topic": f"tags/ID_{i}",
                            "data": {
                                "id": int(i),
                                "corners": corner_list
                            }
                        }
                        if self.gui.client and self.gui.client.running:
                            self.gui.client.send_json(pkt)

                # Si tenemos homografía, proyectar al mundo y calcular pose
                if self.H is not None:
                    tag_world_positions = project_all_tags_to_world(self.H, tag_centers_img)

                    for robot_id in range(MAX_ROBOTS):
                        pose = estimate_robot_pose(robot_id, tag_world_positions)
                        if pose is None:
                            continue
                        x, y, theta = pose

                        data = {
                            "robot_id": robot_id,
                            "x": x,
                            "y": y,
                        }
                        if theta is not None:
                            data["theta_rad"] = theta
                            data["theta_deg"] = math.degrees(theta)
                        else:
                            data["theta_rad"] = None
                            data["theta_deg"] = None

                        pkt_pose = {
                            "action": "PUB",
                            "topic": f"robots/robot{robot_id}/pose",
                            "data": data
                        }

                        if self.gui.client and self.gui.client.running:
                            self.gui.client.send_json(pkt_pose)

            # Actualizar frame para la GUI (video con dibujos)
            self.latest_frame = frame

        self.cap.release()

    def stop(self):
        self.running = False


class PubSubClient:
    def __init__(self, host="localhost", port=5051, log_func=None):
        self.host = host
        self.port = port
        self.sock = None
        self.running = False
        self.thread = None
        self.log = log_func or (lambda msg: print(msg))

    def connect(self):
        if self.running:
            self.log("Ya está conectado.")
            return True
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.running = True
            self.thread = threading.Thread(target=self._recv_loop, daemon=True)
            self.thread.start()
            self.log(f"Conectado a {self.host}:{self.port}")
            return True
        except Exception as e:
            self.log(f"Error de conexión: {e}")
            return False

    def disconnect(self):
        self.running = False
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                self.sock.close()
            except:
                pass
        self.sock = None
        self.log("Desconectado del broker")

    def send_json(self, obj):
        if not self.sock:
            self.log("No conectado")
            return
        try:
            data = json.dumps(obj) + "\n"
            self.sock.send(data.encode("utf-8"))
            self.log(f"→ Enviado: {data.strip()}")
        except Exception as e:
            self.log(f"Error al enviar: {e}")

    def _recv_loop(self):
        buf = b""
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                buf += data
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    text = line.decode("utf-8").strip()
                    if not text:
                        continue
                    try:
                        obj = json.loads(text)
                        self.log(f"← Recibido: {json.dumps(obj)}")
                    except Exception:
                        self.log(f"← (texto) {text}")
            except Exception:
                break
        self.disconnect()


# -----------------------------
# GUI con Tkinter
# -----------------------------
class PubSubGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente Pub/Sub TCP")
        self.client = None

        # --- FRAME DE VIDEO ---
        frm_video = ttk.LabelFrame(root, text="Cámara + ArUco", padding=5)
        frm_video.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

        self.lbl_video = ttk.Label(frm_video)
        self.lbl_video.pack()

        # iniciar hilo de cámara
        self.video_thread = CameraThread(self)
        self.video_thread.start()
        self.update_video()

        # Frame de conexión
        frm_conn = ttk.Frame(root, padding=5)
        frm_conn.pack(fill=tk.X)
        ttk.Label(frm_conn, text="Host:").pack(side=tk.LEFT)
        self.host_var = tk.StringVar(value="localhost")
        ttk.Entry(frm_conn, textvariable=self.host_var, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Label(frm_conn, text="Puerto:").pack(side=tk.LEFT)
        self.port_var = tk.StringVar(value="5051")
        ttk.Entry(frm_conn, textvariable=self.port_var, width=6).pack(side=tk.LEFT, padx=2)
        self.btn_conn = ttk.Button(frm_conn, text="Conectar", command=self.toggle_connection)
        self.btn_conn.pack(side=tk.LEFT, padx=5)

        # Frame de suscripción/publicación
        frm_io = ttk.LabelFrame(root, text="Mensajes", padding=5)
        frm_io.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(frm_io, text="Tópico:").pack(anchor="w")
        self.topic_var = tk.StringVar(value="UDFJC/emb1/robot0/RPi/state")
        ttk.Entry(frm_io, textvariable=self.topic_var, width=60).pack(fill=tk.X, padx=2)

        ttk.Label(frm_io, text="Payload JSON:").pack(anchor="w")
        self.txt_payload = scrolledtext.ScrolledText(frm_io, height=6)
        self.txt_payload.pack(fill=tk.BOTH, padx=2, pady=2)
        self.txt_payload.insert("1.0", json.dumps({
            "v": 0.2,
            "w": 0.0,
            "alfa0": 0,
            "alfa1": 45,
            "alfa2": 30,
            "duration": 2.0
        }, indent=2))

        frm_btns = ttk.Frame(frm_io)
        frm_btns.pack(fill=tk.X, pady=3)
        ttk.Button(frm_btns, text="Suscribirse", command=self.subscribe).pack(side=tk.LEFT, padx=2)
        ttk.Button(frm_btns, text="Publicar", command=self.publish).pack(side=tk.LEFT, padx=2)
        ttk.Button(frm_btns, text="Prueba automática", command=self.auto_test).pack(side=tk.LEFT, padx=5)

        # Log
        frm_log = ttk.LabelFrame(root, text="Log", padding=5)
        frm_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.txt_log = scrolledtext.ScrolledText(frm_log, height=15, state="normal")
        self.txt_log.pack(fill=tk.BOTH, expand=True)

    def update_video(self):
        frame = self.video_thread.latest_frame
        if frame is not None:
            rgb = cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1)
            img = Image.fromarray(rgb)
            self.photo = ImageTk.PhotoImage(image=img)
            self.lbl_video.config(image=self.photo)
        self.root.after(30, self.update_video)

    def on_close(self):
        if hasattr(self, "video_thread"):
            self.video_thread.stop()
        self.root.destroy()

    # -------------------------
    # Funciones GUI
    # -------------------------
    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.txt_log.insert(tk.END, f"[{ts}] {msg}\n")
        self.txt_log.see(tk.END)

    def toggle_connection(self):
        if self.client and self.client.running:
            self.client.disconnect()
            self.client = None
            self.btn_conn.config(text="Conectar")
        else:
            host = self.host_var.get().strip()
            port = int(self.port_var.get().strip())
            self.client = PubSubClient(host, port, log_func=self.log)
            ok = self.client.connect()
            if ok:
                self.btn_conn.config(text="Desconectar")

    def subscribe(self):
        if not self.client:
            self.log("No conectado.")
            return
        topic = self.topic_var.get().strip()
        if not topic:
            self.log("Debe ingresar un tópico.")
            return
        pkt = {"action": "SUB", "topic": topic}
        self.client.send_json(pkt)

    def publish(self):
        if not self.client:
            self.log("No conectado.")
            return
        topic = self.topic_var.get().strip()
        txt = self.txt_payload.get("1.0", tk.END).strip()
        try:
            data = json.loads(txt)
        except Exception as e:
            self.log(f"JSON inválido: {e}")
            return
        pkt = {"action": "PUB", "topic": topic, "data": data}
        self.client.send_json(pkt)

    def auto_test(self):
        if not self.client:
            self.log("Debe conectarse primero.")
            return

        # Tópicos base
        topic_state = "UDFJC/emb1/robot0/RPi/state"
        topic_seq = "UDFJC/emb1/robot0/RPi/sequence"

        # Suscripción a ambos
        self.client.send_json({"action": "SUB", "topic": topic_state})
        self.client.send_json({"action": "SUB", "topic": topic_seq})

        # Payloads
        state_payload = {
            "v": 0.2, "w": 0.0, "alfa0": 0, "alfa1": 45, "alfa2": 30, "duration": 2.0
        }
        seq_payload = {
            "action": "create",
            "sequence": {
                "name": "saludo",
                "states": [
                    {"v": 10, "w": 0, "alfa0": 0, "alfa1": 0, "alfa2": 0, "duration": 1.0},
                    {"v": 15.7, "w": 90, "alfa0": 0, "alfa1": 0, "alfa2": 0, "duration": 1.0},
                    {"v": 0, "w": 0, "alfa0": -90, "alfa1": 0, "alfa2": 0, "duration": 1.0},
                ]
            }
        }

        # Publicar ambos mensajes
        self.client.send_json({"action": "PUB", "topic": topic_state, "data": state_payload})
        self.client.send_json({"action": "PUB", "topic": topic_seq, "data": seq_payload})
        self.client.send_json({"action": "PUB", "topic": topic_seq,
                               "data": {"action": "execute_now", "name": "saludo"}})

        self.log("→ Prueba automática enviada.")


# -----------------------------
# Main
# -----------------------------
def main():
    root = tk.Tk()
    app = PubSubGUI(root)
    root.geometry("800x700")
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
