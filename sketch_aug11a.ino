int x;
void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1);
 pinMode(2, OUTPUT);
 pinMode(4, OUTPUT);
 pinMode(7, OUTPUT);
 pinMode(8, OUTPUT);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 switch(x){
  case 1:
    digitalWrite(2, HIGH);
    Serial.print("BLUE");
    break;
  case 2:
    digitalWrite(4, HIGH);
    Serial.print("RED");
    break;
  case 3:
    digitalWrite(7, HIGH);
    Serial.print("GREEN");
    break;
  case 4:
    digitalWrite(8, HIGH);
    Serial.print("YELLOW");
    break;
  default:
    Serial.print("ERROR");
    break;
 }
 delay(1000);
 digitalWrite(2, LOW);
 digitalWrite(4, LOW);
 digitalWrite(7, LOW);
 digitalWrite(8, LOW);
 Serial.print("A");
}
