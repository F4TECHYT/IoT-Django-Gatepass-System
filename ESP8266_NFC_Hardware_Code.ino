#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <SPI.h>
#include <MFRC522.h>

// ---------------------------------------------------------
// CONFIGURATION
// ---------------------------------------------------------

// Wi-Fi Credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Django Server Configuration
// Important: Make sure your Django server is running on 0.0.0.0
// e.g., python manage.py runserver 0.0.0.0:8000
const char* serverIP = "192.168.1.100"; // Replace with your computer's local IP address
const int serverPort = 8000;

// Hardware Pins for NodeMCU ESP8266
#define RST_PIN  0  // D3
#define SS_PIN   4  // D2

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Initialize SPI bus and MFRC522 reader
  SPI.begin();
  mfrc522.PCD_Init();
  
  Serial.println("\n--- Gatepass NFC Hardware Setup ---");
  Serial.println("Connecting to Wi-Fi...");
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWi-Fi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println("Ready to scan NFC tags...");
}

void loop() {
  // Check if a new card is present
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Read the card serial number (UID)
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Convert the UID bytes to a Hex string
  String tagUID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tagUID += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    tagUID += String(mfrc522.uid.uidByte[i], HEX);
  }
  
  // Convert to uppercase (optional, depending on server requirements)
  tagUID.toUpperCase();

  Serial.print("\nTag Scanned UID: ");
  Serial.println(tagUID);
  
  // Send the UID to the Django server
  sendToServer(tagUID);

  // Halt PICC to avoid reading the same card multiple times instantly
  mfrc522.PICC_HaltA();
  // Stop encryption on PCD
  mfrc522.PCD_StopCrypto1();
  
  // Wait before next scan
  delay(2000);
}

void sendToServer(String uid) {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    
    // Construct the API URL
    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/api/nfc_scan?id=" + uid;
    
    Serial.print("Sending request to: ");
    Serial.println(url);
    
    // Initialize the HTTP request
    http.begin(client, url);
    
    // Perform GET request
    int httpResponseCode = http.GET();
    
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response Code: ");
      Serial.println(httpResponseCode);
      
      String payload = http.getString();
      Serial.println("Server Response Payload: ");
      Serial.println(payload);
      
      // Here you can parse the JSON payload to trigger a relay for the gate
      // e.g., if payload contains "status":"success" -> triggerGate();
    } else {
      Serial.print("Error Code: ");
      Serial.println(httpResponseCode);
    }
    
    // Free resources
    http.end();
  } else {
    Serial.println("Error: Wi-Fi Disconnected!");
  }
}
