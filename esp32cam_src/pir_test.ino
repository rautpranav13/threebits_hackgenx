#define LED_PIN 33  
#define PIR_PIN 2  

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  Serial.println("PIR Motion Detection Test Starting...");
}

void loop() {
  int motionDetected = digitalRead(PIR_PIN);

  if (motionDetected == HIGH) {
    Serial.println("Motion Detected! Turning LED ON");
    digitalWrite(LED_PIN, HIGH);
  } else {
    Serial.println("No Motion. Turning LED OFF");
    digitalWrite(LED_PIN, LOW);
  }

  delay(1000); // Wait for 1 second before checking again
}