#include <DHT.h>

#define LED_PIN 33   
#define PIR_PIN 2    
#define LDR_PIN 16   
#define DHTPIN 13    
#define DHTTYPE DHT22  

DHT dht(DHTPIN, DHTTYPE);  

int lastLDRValue = -1;  

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(LDR_PIN, INPUT);  

  // Initialize DHT22 sensor
  dht.begin();

  Serial.println("PIR + LDR + DHT22 Test Starting...");
}

void loop() {
  // Read LDR
  int ldrValue = analogRead(LDR_PIN);
  bool ldrValid = (ldrValue > 50 && ldrValue < 4000);  // Safe range

  if (!ldrValid || ldrValue == lastLDRValue) {
    Serial.print("⚠️ Possible LDR issue. Value: ");
    Serial.println(ldrValue);
  } else {
    Serial.print("📊 LDR Value: ");
    Serial.println(ldrValue);
  }

  lastLDRValue = ldrValue;  // Update for next check

  // Read PIR sensor
  int motionDetected = digitalRead(PIR_PIN);

  // Act based on motion
  if (motionDetected == HIGH) {
    Serial.println("🚶 Motion Detected! Turning LED ON");
    digitalWrite(LED_PIN, HIGH);
  } else {
    Serial.println("🛑 No Motion. Turning LED OFF");
    digitalWrite(LED_PIN, LOW);
  }

  // Read DHT22 sensor (Temperature & Humidity)
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("❌ Failed to read from DHT22");
  } else {
    Serial.print("🌡️ Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C  | 💧 Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  }

  delay(100000);  // Wait for 1 second before next reading
}