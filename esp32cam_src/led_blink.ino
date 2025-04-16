#define LED_PIN 33  // Onboard red LED on ESP32-CAM

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("LED Blink Test Starting...");
}

void loop() {
  Serial.println("LED ON");
  digitalWrite(LED_PIN, HIGH);
  delay(1000);

  Serial.println("LED OFF");
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}