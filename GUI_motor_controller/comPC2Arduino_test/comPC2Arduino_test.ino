void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // set the baud rate of 9600 bps
  Serial.println("Ready"); // print "Ready" once
  pinMode (13, OUTPUT); // configure the on-board LED as output
}

void loop() {
  // put your main code here, to run repeatedly
  
  if (Serial.available())// if the receiver is full
  {
    switch (Serial.read())
    {
      case '0': digitalWrite(13, LOW);
                break;
      case '1': digitalWrite(13, HIGH);
                break;
      default:  break;
    }
    delay(1); // delay for 0.1 second for each loop
  }

}
