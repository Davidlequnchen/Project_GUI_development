const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int analogOutPin = 9; // Analog output pin that the LED is attached to

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // set the baud rate of 9600 bps
  Serial.println("Ready"); // print "Ready" once
  pinMode (13, OUTPUT); // configure the on-board LED as output
}

void loop() {
  // put your main code here, to run repeatedly:

  char inByte = ' '; 
  int requesr_received;


  if (Serial.available())// if the receiver is full
  {  
    // String(inByte) = Serial.readString();  // read the data
    requesr_received = Serial.read();
    Serial.print("Command received: ");
    switch (requesr_received) // read the data, one bit at a time, after reading the data will be destroyed. Alter: Serial.readBytes(buffer, length) 
    {
      case '0': 
                digitalWrite(13, LOW);
                Serial.println("0"); // send the data back in a new line so that it is not all one long line
                break;
                
      case '1': 
                digitalWrite(13, HIGH);
                Serial.println("1"); // send the data back in a new line so that it is not all one long line
                break;
                
      default:  
                Serial.print(requesr_received); // send the data back in a new line so that it is not all one long line
                break;
    }
  }

  // read the analog voltage in value:
  sensorValue = analogRead(analogInPin);

  // print the results to the Serial Monitor:
//  Serial.print("sensor = ");
  Serial.println(sensorValue);
  
  delay(2); // delay for 2 miliseconds for each loop

}
