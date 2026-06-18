const int ledPin = 13;
String inputString = "";
int brightness = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // --- Receive from Python ---
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      brightness = inputString.toInt();
      brightness = constrain(brightness, 0, 255);
      Serial.print("Brightness set to: ");
      Serial.println(brightness);
      inputString = "";
    } else {
      inputString += inChar;
    }
  }

  // --- Simulate PWM on pin 13 (not a hardware PWM pin) ---
  int onTime = map(brightness, 0, 255, 0, 1000);  // in microseconds
  int offTime = 1000 - onTime;

  digitalWrite(ledPin, HIGH);
  delayMicroseconds(onTime);
  digitalWrite(ledPin, LOW);
  delayMicroseconds(offTime);
}
