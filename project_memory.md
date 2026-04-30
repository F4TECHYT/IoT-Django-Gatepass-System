# Gatepass System - Project Memory

## 1. Project Overview
The Gatepass system is a comprehensive solution for managing student and staff gate pass requests, approvals, and physical gate access. It consists of a Django-based web application backend and an ESP8266-based NFC hardware scanner that verifies access in real-time. The system has recently been optimized by cleaning up redundant files to improve maintainability.

## 2. Technology Stack
- **Backend Framework:** Django (Python 3.x)
- **Database Architecture:** MySQL/MariaDB via `PyMySQL`. Notably, the project uses **raw SQL queries** directly in `views.py` for database operations, bypassing Django's built-in ORM (`models.py` is largely empty).
- **Hardware Integration:** ESP8266 (NodeMCU) microcontroller paired with an MFRC522 RFID/NFC reader module (Code resides in `ESP8266_NFC_Hardware_Code.ino`).
- **Frontend:** HTML/CSS templates rendered via Django views.

## 3. Core Architecture
- **Database Interaction:** The `gpass/views.py` file is the central hub for business logic, handling routing and executing raw SQL `cursor.execute(...)` statements.
- **Hardware Communication:** The ESP8266 connects to the local network and makes HTTP GET requests to the Django server's API endpoint (e.g., `http://<SERVER_IP>:8000/api/nfc_scan?id=<CARD_UID>`). The server checks the database and returns a JSON response indicating whether access is granted or denied.
- **Network Configuration:** The Django development server must be run on `0.0.0.0:8000` to allow the ESP8266 module on the same network to communicate with it.

## 4. Key Workflows & User Roles
- **Admin Role:**
  - Secure login.
  - Manage and view all registered students and staff.
  - **NFC Tag Assignment:** Link physical NFC card UIDs to specific student or staff profiles in the database.
  - View comprehensive logs of gate passes and real-time movement (In/Out) history.
- **Staff Role:**
  - Registration and login workflows.
  - Review, approve, or reject gate pass requests submitted by students.
- **Student Role:**
  - Register with enrollment details, including profile pictures.
  - Submit detailed gate pass requests (reason, expected out time, expected in time).
  - Track the status of requests (Pending, Approved, Rejected).

## 5. Important Project Files
- `User_Manual_and_Instructions.md`: Detailed system documentation, including server setup instructions and hardware wiring diagrams.
- `ESP8266_NFC_Hardware_Code.ino`: The C++ source code for the NodeMCU, handling Wi-Fi connection, NFC reading, and HTTP requests.
- `gpass/views.py`: Contains the entirety of the application's request handling, authentication logic, and raw database queries (over 1,400 lines).
- `manage.py`: The standard Django command-line utility.

## 6. Current Development State
The project repository was recently streamlined to remove redundant scripts, debugging files, and old instruction manuals. The current focus is on maintaining a robust connection between the ESP8266 hardware and the Django backend, ensuring accurate mapping of NFC tags, and providing a seamless gate access experience.
