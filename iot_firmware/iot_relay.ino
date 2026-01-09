#include <FS.h>                   // Must be first
#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>          // https://github.com/tzapu/WiFiManager
#include <ArduinoJson.h>          // https://github.com/bblanchon/ArduinoJson
#include <PubSubClient.h>

// --- Configuration ---
#define RELAY_PIN 4               // D2 is usually GPIO 4 on NodeMCU/Wemos
#define CONFIG_FILE "/config.json"

// --- Global Variables ---
char mqtt_server[40] = "202.74.74.42";
char mqtt_port[6] = "1883";
char mqtt_topic[50] = "gesture/control";

bool shouldSaveConfig = false;

WiFiClient espClient;
PubSubClient client(espClient);

// --- Callback for Save Config ---
void saveConfigCallback () {
  Serial.println("Should save config");
  shouldSaveConfig = true;
}

// --- MQTT Callback ---
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("]Payload: ");

  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  // Logic: 1 = ON, 0 = OFF (Active High)
  if (message == "1") {
    digitalWrite(RELAY_PIN, HIGH);
    Serial.println("Relay ON");
  } else if (message == "0") {
    digitalWrite(RELAY_PIN, LOW);
    Serial.println("Relay OFF");
  }
}

// --- Load Config from FS ---
void loadConfig() {
  if (SPIFFS.begin()) {
    if (SPIFFS.exists(CONFIG_FILE)) {
      File configFile = SPIFFS.open(CONFIG_FILE, "r");
      if (configFile) {
        size_t size = configFile.size();
        std::unique_ptr<char[]> buf(new char[size]);
        configFile.readBytes(buf.get(), size);
        
        DynamicJsonDocument json(1024);
        DeserializationError error = deserializeJson(json, buf.get());
        
        if (!error) {
          strcpy(mqtt_server, json["mqtt_server"]);
          strcpy(mqtt_port, json["mqtt_port"]);
          strcpy(mqtt_topic, json["mqtt_topic"]);
        }
      }
    }
  } else {
    Serial.println("failed to mount FS");
  }
}

// --- Save Config to FS ---
void saveConfig() {
  DynamicJsonDocument json(1024);
  json["mqtt_server"] = mqtt_server;
  json["mqtt_port"] = mqtt_port;
  json["mqtt_topic"] = mqtt_topic;

  File configFile = SPIFFS.open(CONFIG_FILE, "w");
  if (!configFile) {
    Serial.println("failed to open config file for writing");
  }
  serializeJson(json, configFile);
  configFile.close();
}

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // Default OFF

  // 1. Load Config
  loadConfig();

  // 2. Setup WiFiManager
  WiFiManager wifiManager;
  wifiManager.setSaveConfigCallback(saveConfigCallback);

  // Custom Parameters
  WiFiManagerParameter custom_mqtt_server("server", "MQTT Server", mqtt_server, 40);
  WiFiManagerParameter custom_mqtt_port("port", "MQTT Port", mqtt_port, 6);
  WiFiManagerParameter custom_mqtt_topic("topic", "MQTT Topic", mqtt_topic, 50);

  wifiManager.addParameter(&custom_mqtt_server);
  wifiManager.addParameter(&custom_mqtt_port);
  wifiManager.addParameter(&custom_mqtt_topic);

  // Connect or Portal
  if (!wifiManager.autoConnect("Gesture_Lamp_AP")) {
    Serial.println("failed to connect and hit timeout");
    delay(3000);
    ESP.reset();
    delay(5000);
  }

  // 3. Save Config if needed
  if (shouldSaveConfig) {
    strcpy(mqtt_server, custom_mqtt_server.getValue());
    strcpy(mqtt_port, custom_mqtt_port.getValue());
    strcpy(mqtt_topic, custom_mqtt_topic.getValue());
    saveConfig();
  }

  Serial.println("Connected to WiFi!");
  
  // 4. Setup MQTT
  client.setServer(mqtt_server, atoi(mqtt_port));
  client.setCallback(callback);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
