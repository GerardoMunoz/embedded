# REST, WebHook, JavaScript Methods and WebSocket

## 1. REST

* **REST (Representational State Transfer):** an **architectural style** for designing distributed systems.

* **REST is a set of best practices** that defines how to use HTTP consistently for clean, scalable APIs.

Without REST, you might use HTTP in an arbitrary way, for example:

```
POST /getUser?id=123
```

That *works* in HTTP, but it’s not RESTful design. In REST, this would be modeled as:

```
GET /users/123
```

---

👉 In summary: **REST doesn’t add anything “new” to HTTP, but establishes conventions and an architectural style to use HTTP consistently.**

* Example of a REST API:

  ```http
  GET https://api.server.com/sensors/temperature
  ```

  Response:

  ```json
  { "temp": 22.5, "unit": "C" }
  ```

* Normally, a REST API uses multiple HTTP methods (**GET, POST, PUT, DELETE, etc.**) to represent actions on resources, not just GET.

* Summary:

  * **REST → theory (principles).**
  * **RESTful API → an implementation that follows REST principles strictly.**
  * **REST API → a practical implementation (sometimes partial) of REST.**

### **Examples of Public REST APIs with GET**

#### Met.no (Norwegian Meteorological Institute)

* Official API also used by apps like Yr.no.
* Example forecast for Oslo:

  ```
  https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.91&lon=10.75
  ```

#### USGS Earthquake API

* Real-time seismic information.
* Example: last earthquakes M>4.5:

  ```
  https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson
  ```

---

## 2. WebHook
A webhook is just:

You tell the provider (via HTTP) the URL where you want to receive events.

The provider sends you HTTP requests (usually POST) whenever an event happens.

So the “subscription” step is usually an HTTP request you make to the provider’s API.

* **Event-driven communication mechanism.**
* Instead of the client polling the server, the server sends data **when an event occurs**.
* Used in:

  * Service integrations (e.g., GitHub → notification to a server on push).
  * IoT → a device can receive real-time alerts.
  * **Discord:** WebHooks allow external apps to send automated messages to a channel.
* General example:

  * Service A (sensor server) sends a POST to Service B’s URL when new data arrives.

  ```http
  POST /webhook HTTP/1.1
  Host: my-server.com
  Content-Type: application/json

  { "sensor": "temp", "value": 22.5 }
  ```

### WebHook as Pub/Sub Pattern

* A WebHook can be seen as a simple form of **Pub/Sub (Publish/Subscribe):**

  * **Publisher:** the server/service that generates the event.
  * **Subscriber:** the app exposing an endpoint that receives notifications.
* Differences vs. more complex Pub/Sub systems (e.g., MQTT, Kafka):

  * WebHook → direct HTTP communication between services.
  * Pub/Sub → uses a **broker** between publishers and subscribers.
* In IoT, WebHooks are useful for **event notifications**, while MQTT is better for **continuous data streams**.
* There isn’t a single universal standard HTTP message for subscribing to a webhook. It actually depends on the service you’re integrating with. But most providers follow some common patterns built on top of plain HTTP.




### Typical patterns

REST-style subscription
You send a POST request to the provider’s API, telling it your webhook URL:

POST /webhooks HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "url": "https://myapp.com/webhook",
  "events": ["user.created", "user.deleted"]
}


Then the provider might answer with 201 Created and return the webhook ID.

Challenge/verification handshake
Many providers (e.g., GitHub, Slack, Stripe) send a verification request (often a GET or POST) to your webhook URL to confirm you control it.
Example (Stripe style):

POST https://myapp.com/webhook
{
  "type": "verification",
  "challenge": "abc123"
}


Your server must reply with that challenge token.

Manual configuration
Sometimes you don’t subscribe via HTTP at all—you go into the provider’s dashboard (UI), paste your webhook URL, and they handle the rest.

### Standards

There are some efforts at standardizing this:

WebSub (W3C)
 defines a publish/subscribe system over HTTP.

But in practice, most webhook systems are custom, with similar but slightly different subscription flows.




### WebHooks in Discord

* Discord provides a unique URL for each channel WebHook.
* Messages are always sent via **HTTP POST**.
* Example payload:

  ```http
  POST https://discord.com/api/webhooks/WEBHOOK_ID/WEBHOOK_TOKEN
  Content-Type: application/json

  { "content": "Hello from my IoT app!" }
  ```
* Supports simple text messages, embeds, or more complex notifications.

---

## 3. JavaScript Methods for Communication

### fetch()

* Modern **JavaScript** function for making HTTP requests.
* Based on **Promises** → cleaner and easier than older alternatives.
* By default, `fetch()` uses **GET**, but it can be configured for **POST, PUT, DELETE, PATCH, etc.**

### XMLHttpRequest (XHR)

* Older JavaScript API for HTTP requests.
* Foundation of the **AJAX** concept.
* More verbose and callback-based compared to `fetch()`.

### Other Methods

* **window\.location.reload()** → Reloads the current page.
* **HTML Forms** → Submitting a form sends data or reloads.
* **Server-Sent Events (SSE):** → One-way stream from server to browser.
* **window\.location.href = 'url'** → Redirects to another URL.

---

## 4. WebSocket

* **Protocol for real-time, bidirectional communication** over a single TCP connection.
* Unlike REST (request/response), WebSocket allows continuous data exchange.
* Commonly used in **IoT**, **chat apps**, **real-time dashboards**.

Example:

```javascript
import network
import socket
import time
import ubinascii
import uhashlib

# === CONFIG ===
SSID = "Ejemplo"
PASSWORD = "12345678"

# === CONNECT WIFI ===
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(0.5)
print("Connected:", wlan.ifconfig())

# === HTML PAGE ===
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Pico W WebSocket Demo</title>
</head>
<body>
  <h2>WebSocket Echo Demo</h2>
  <input id="msg" type="text" placeholder="Type a message">
  <button onclick="sendMsg()">Send</button>
  <ul id="log"></ul>

  <script>
    let ws = new WebSocket("ws://" + location.host + "/");
    ws.onopen = () => log("Connected to WebSocket");
    ws.onmessage = (e) => log("Received: " + e.data);
    ws.onclose = () => log("Connection closed");

    function sendMsg() {
      let m = document.getElementById("msg").value;
      ws.send(m);
      log("Sent: " + m);
    }

    function log(text) {
      let li = document.createElement("li");
      li.textContent = text;
      document.getElementById("log").appendChild(li);
    }
  </script>
</body>
</html>
"""

# === HELPERS ===
def websocket_handshake(client, request):
    """Perform WebSocket upgrade handshake"""
    for line in request.split("\r\n"):
        if line.startswith("Sec-WebSocket-Key:"):
            key = line.split(":", 1)[1].strip()
            break
    else:
        return False

    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    sha1 = uhashlib.sha1(key.encode() + GUID.encode())
    accept_key = ubinascii.b2a_base64(sha1.digest()).decode().strip()

    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Accept: {}\r\n\r\n".format(accept_key)
    )
    client.send(response.encode())
    return True

def recv_ws_frame(client):
    """Receive a WebSocket frame (only supports small text frames)"""
    hdr = client.recv(2)
    if not hdr:
        return None
    length = hdr[1] & 0x7F
    mask = client.recv(4)
    data = bytearray(client.recv(length))
    for i in range(length):
        data[i] ^= mask[i % 4]
    return data.decode()

def send_ws_frame(client, msg):
    """Send a WebSocket text frame"""
    frame = bytearray([0x81, len(msg)])
    frame.extend(msg.encode())
    client.send(frame)

# === SERVER ===
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Listening on", addr)

while True:
    cl, addr = s.accept()
    print("Client connected from", addr)
    request = cl.recv(1024).decode()

    if "Upgrade: websocket" in request:
        if websocket_handshake(cl, request):
            print("WebSocket handshake complete")
            while True:
                try:
                    msg = recv_ws_frame(cl)
                    if msg is None:
                        break
                    print("Got:", msg)
                    send_ws_frame(cl, "Echo: " + msg)
                except Exception as e:
                    print("Connection closed:", e)
                    break
    else:
        # Serve the HTML page
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + HTML_PAGE
        cl.send(response.encode())
    cl.close()


```

* Advantage over REST:

  * REST → stateless, one request → one response.
  * WebSocket → persistent, supports event-driven flows.

---



