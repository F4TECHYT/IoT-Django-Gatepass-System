# Gatepass System - Full Instruction & User Manual

## 1. System Overview
The Gatepass system is a complete solution for managing student and staff gate pass requests, approvals, and physical gate access. It consists of a Django-based web application backend and an ESP8266-based NFC hardware scanner that verifies access in real-time.

---

## 2. Server Setup & Running

### Prerequisites
- Python 3.x installed
- Required Python packages (install via `pip install django PyMySQL`)
- A MySQL/MariaDB database (or SQLite depending on your settings)

### How to Run the Server
1. Open your terminal or command prompt.
2. Navigate to the project root directory (`e:\Main Project\Gatepass`).
3. Apply any pending database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Start the Django development server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
   *Note: Using `0.0.0.0` allows the server to be accessible from other devices on the same network (like the ESP8266).*

---

## 3. Website User Manual

### Roles
There are three main roles in the system: **Admin**, **Staff**, and **Student**.

### Admin Workflows
- **Login:** Access the admin portal using the admin credentials.
- **Manage Users:** View registered students and staff.
- **Assign NFC Tags:** Go to "Assign NFC Tag" to link a physical NFC card's UID to a specific student or staff member.
- **Gate Pass History:** View the complete log of all gate passes and movement (In/Out) history.

### Staff Workflows
- **Registration & Login:** Register as staff and log in.
- **Review Requests:** View and approve or reject gate pass requests submitted by students.

### Student Workflows
- **Registration & Login:** Register as a student with your enrollment details and log in.
- **Request Gatepass:** Submit a gate pass request detailing the reason and time.
- **View Status:** Track whether your request is pending, approved, or rejected.

---

## 4. Hardware Details

The hardware component consists of an **ESP8266 (NodeMCU)** microcontroller and an **MFRC522** RFID/NFC reader module.

### Wiring Diagram (ESP8266 to MFRC522)
| MFRC522 Pin | ESP8266 (NodeMCU) Pin |
|-------------|-----------------------|
| SDA (SS)    | D2 (GPIO4)            |
| SCK         | D5 (GPIO14)           |
| MOSI        | D7 (GPIO13)           |
| MISO        | D6 (GPIO12)           |
| IRQ         | *Not Connected*       |
| GND         | GND                   |
| RST         | D3 (GPIO0)            |
| 3.3V        | 3V3                   |

*WARNING: The MFRC522 operates on 3.3V. Do not connect it to the 5V pin as it will damage the module.*

### How the Hardware Works
1. The ESP8266 connects to the local Wi-Fi network.
2. When an NFC card is tapped, the MFRC522 reads the card's Unique Identifier (UID).
3. The ESP8266 makes an HTTP GET request to the Django server:
   `http://<SERVER_IP>:8000/api/nfc_scan?id=<CARD_UID>`
4. The server checks if the UID is assigned and if the person has an approved gate pass, then returns a JSON response indicating success or failure.
5. The ESP8266 can be expanded to trigger a relay (to open a physical gate or turnstile) based on the server's response.
