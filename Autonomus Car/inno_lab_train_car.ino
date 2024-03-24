// Arduino Code for conn

#define trigPin 8
#define echoPin 7

#define tp 0
#define ep 1

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(tp, OUTPUT);
  pinMode(ep, INPUT);
}

void loop() {
  long duration, distance, du, di;

  digitalWrite(trigPin, LOW);
  digitalWrite(tp,LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  digitalWrite(tp,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  digitalWrite(tp,LOW);
  duration = pulseIn(echoPin, HIGH);
  du = pulseIn(ep,HIGH);
  distance = duration * 0.034 / 2;
  di = du * 0.034 / 2;
  Serial.print("ne ");
  Serial.println(distance);
  Serial.print("nw ");
  Serial.println(di);

  delay(1000);  

 
}
