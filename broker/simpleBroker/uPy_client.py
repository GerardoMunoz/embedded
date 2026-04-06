# 
# ## 🧪 Homework – Embedded Pub/Sub Client
# 
# ### ✅ Setup (Required – Do First)
# 
# 1. Update the WiFi configuration
# 
#    * Change the network name (`SSID`) in the code
# 
# 2. Create a `.env` file in your device
# 
#    * Store your WiFi password inside
# 
# 3. Configure the broker connection
# 
#    * Update the Broker IP address to match your computer
# 
# ---
# 
# ### 🚀 Core Tasks (Required)
# 
# 4. Run the system and verify:
# 
#    * Device connects to WiFi
#    * Frames are sent to the broker
#    * Messages are received in the web client
# 
# 5. Debug any issues:
# 
#    * Check serial output
#    * Verify JSON structure
#    * Validate base64 decoding in the browser
# 
# ---
# 
# ### 🔧 Extensions (Choose at least ONE)
# 
# 6. Improve the communication system
# 
#    * Add a local Pub/Sub mechanism (callbacks per topic)
# 
# 7. Improve performance
# 
#    * Replace base64 with binary transmission **(advanced)**
# 
# 8. Camera improvements
# 
#    * Replace the fake camera with the real OV7670 camera module
#    * Optionally capture frames using `_thread`
# 
# 9. Robot interaction
# 
#    * Create a new Task to control:
# 
#      * servos
#      * LEDs
#      * or other actuators
# 
# ---
# 
# ### 🧠 Reflection (Short Answer)
# 
# 10. Answer briefly:
# 
# * What is the advantage of using a Scheduler instead of a simple loop?
# * What problems does Pub/Sub solve in embedded systems?
# 
#



# To Do Now
###########
# Change the WiFi network name
# Create .env file in the RPi Pico with the password
# Update the Broker IP 

# To Do Later
#############
# Update to allow a local bus to subscribe to callbacks.
# OV7670 camera update; to read data on the other `_thread`.
# Creation of another task to interact with the robot.


# =============================================================
# MICRO PYTHON PUBSUB CLIENT WITH SCHEDULER
# =============================================================

import network, time, json, gc
import usocket as socket
import ubinascii
from machine import Timer


# =========================================================
# WIFI
# =========================================================
class WiFiManager:
    def __init__(self, ssid, password_file=".env"):
        self.ssid = ssid
        with open(password_file) as f:
            self.password = f.read().strip()

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self):
        print("Conectando a WiFi...")
        if not self.wlan.isconnected():
            self.wlan.connect(self.ssid, self.password)
            while not self.wlan.isconnected():
                time.sleep(0.5)

        print("✅ WiFi OK:", self.wlan.ifconfig()[0])



# =========================================================
# SOCKET CLIENT
# =========================================================
class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        print("🔌 Conectando al broker...")
        addr = socket.getaddrinfo(self.host, self.port)[0][-1]
        self.sock = socket.socket()
        self.sock.connect(addr)
        self.sock.settimeout(0.1)
        print("✅ Conectado")

    def ensure(self):
        if self.sock is None:
            self.connect()

    def send(self, data):
        total = 0
        while total < len(data):
            total += self.sock.send(data[total:])

    def send_json(self, obj):
        self.send((json.dumps(obj) + "\n").encode())

    def close(self):
        try:
            if self.sock:
                self.sock.close()
        except:
            pass
        self.sock = None



# =========================================================
# PUBSUB CLIENT
# =========================================================
#Update to allow a local bus to subscribe to callbacks.
class PubSubClient:
    def __init__(self, socket_client, prefix='UDFJC/emb1/robot0/'):
        self.sock = socket_client
        self.prefix=prefix

    def publish(self, topic, data):
        self.sock.ensure()

        pkt = {
            "action": "PUB",
            "topic": self.prefix+topic,
            "data": data
        }

        self.sock.send_json(pkt)


# =========================================================
# SCHEDULER SYSTEM
# =========================================================
# ⚠ Important limitation
# 
# If a task blocks:
# 
# time.sleep(2)
# 
# 👉 EVERYTHING stops
# 
# So:
# 
# ✔ Keep tasks fast
# ✔ No blocking calls
# ✔ Use state machines if needed


import time

class Task:
    def __init__(self, scheduler, period_ms, priority=1):
        self.period = period_ms
        self.priority = priority
        self.next_run = time.ticks_ms()
        scheduler.add(self)
#     def __init__(self, scheduler, period_ms):
#         self.period = period_ms
#         self.next_run = time.ticks_ms()
#         scheduler.add(self)

    def update(self):
        pass




class Scheduler:
    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)
        self.tasks.sort(key=lambda t: t.priority)

    def run(self):
        while True:
            now = time.ticks_ms()

            for task in self.tasks:
                if time.ticks_diff(now, task.next_run) >= 0:
                    task.update()
                    task.next_run = time.ticks_add(now, task.period)

            gc.collect()
            time.sleep_ms(1)


#################### TASKS #################


class WatchdogTask(Task):
    def __init__(self, scheduler, pubsub, period_ms=10000):
        super().__init__(scheduler, period_ms=10000)

        self.pubsub = pubsub
        #self.flag = False

#         self.timer = Timer()
#         self.timer.init(
#             mode=Timer.PERIODIC,
#             period=period_ms,
#             callback=self._cb
#         )

    #def _cb(self, t):
    #    self.flag = True

    def update(self):
        #if self.flag:
        #    self.flag = False

            self.pubsub.publish(
                "debug/watchdog",
                {"msg": "alive"}
            )

            print("🐶 Watchdog")
            

class CameraPublisherTask(Task):
    # Upgrade to the real ov7670 camera, it could read the data on the other `_thread`
    def __init__(self, scheduler, pubsub, width=40, height=30):
        super().__init__(scheduler, period_ms=2000)

        self.pubsub = pubsub
        self.WIDTH = width
        self.HEIGHT = height
        self.buf = bytearray(width * height * 2)

#        self.last = 0
#        self.interval = 2

    def update(self):
        #now = time.time()

        #if now - self.last > self.interval:
#            gc.collect()

            frame = self._generate_frame()
#            frame_b64 = ubinascii.b2a_base64(frame).decode().strip()
            frame_b64 = ubinascii.b2a_base64(frame).decode().replace("\n", "")

            self.pubsub.publish(
                "camera/frame",
                {
                    "w": self.WIDTH,
                    "h": self.HEIGHT,
                    "frame": frame_b64
                }
            )

            print("📤 Frame")
            #self.last = now

    def _generate_frame(self):
        t = int(time.time()) % 60

        r = (t * 4) % 256
        g = (128 + t * 2) % 256
        b = (255 - t * 3) % 256

        color = self.rgb565(r, g, b)

        hi = (color >> 8) & 0xFF
        lo = color & 0xFF

        for i in range(0, len(self.buf), 2):
            self.buf[i] = hi
            self.buf[i + 1] = lo

        return self.buf

    def rgb565(self, r, g, b):
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)




# =========================================================
# MAIN APP
# =========================================================
class MainApp:
    def __init__(self):

        self.wifi = WiFiManager("Ejemplo") # Change to your WiFi
        self.socket = SocketClient("192.168.1.17", 5051) # Change to the Broker IP
        self.scheduler = Scheduler()
        self.pubsub = PubSubClient(self.socket)
        self.watchdog = WatchdogTask(scheduler=self.scheduler, pubsub=self.pubsub)
        self.camera = CameraPublisherTask(scheduler=self.scheduler, pubsub=self.pubsub, width=40, height=30)

#         # Register tasks
#         self.frame_task = FramePublisherTask(
#             self.scheduler, self.pubsub, self.camera
#         )
# 
#         self.watchdog_task = WatchdogTask(
#             self.scheduler, self.pubsub, self.watchdog
#         )

    def run(self):
        self.wifi.connect()
        print("🚀 Scheduler running...")
        self.scheduler.run()


# =========================================================
# ENTRY POINT
# =========================================================
app = MainApp()
app.run()