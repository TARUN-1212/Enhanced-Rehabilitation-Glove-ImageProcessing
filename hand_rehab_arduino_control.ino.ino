#include <Servo.h>

// Define constants for number of values expected
#define NO_OF_VAL_REC 5        // Number of fingers (thumb + 4 fingers)
#define DIGIT_PER_VAL_REC 1    // Each value is a single digit (0 or 1)

// Create Servo objects for each finger
Servo thumbServo;
Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;

// Array to hold values received from the serial (one per finger)
int valsRec[NO_OF_VAL_REC];

// Total length of the expected string: 5 values + 1 start character ('$')
int stringLength = NO_OF_VAL_REC * DIGIT_PER_VAL_REC + 1;

// Variables to help read serial data
int counter = 0;               // Counter to keep track of characters received
bool counterStart = false;     // Flag to indicate when to start recording
String receivedString;         // Holds the full incoming data string

void setup() {
  Serial.begin(9600);  // Start serial communication

  // Attach servo motors to respective digital pins
  thumbServo.attach(11);
  indexServo.attach(9);
  middleServo.attach(5);
  ringServo.attach(3);
  pinkyServo.attach(6);
}

void loop() {
  receiveData();    // Continuously check for new serial input
  controlServos();  // Update servo positions based on received values
}

// Function to update servo angles based on each finger's status (1 = closed, 0 = open)
void controlServos() {
  thumbServo.write(valsRec[0] == 1 ? 0 : 60);
  indexServo.write(valsRec[1] == 1 ? 0 : 140);
  middleServo.write(valsRec[2] == 1 ? 140 : 0);
  ringServo.write(valsRec[3] == 1 ? 90 : 0);
  pinkyServo.write(valsRec[4] == 1 ? 0 : 160);
}

// Function to receive and parse incoming serial data
// Expected format: $10110 (e.g., $<thumb><index><middle><ring><pinky>)
void receiveData() {
  while (Serial.available()) {
    char c = Serial.read();  // Read one character at a time

    if (c == '$') {
      counterStart = true;   // Start collecting when '$' is received
    }

    if (counterStart) {
      if (counter < stringLength) {
        receivedString += c;  // Append character to full string
        counter++;
      }

      if (counter >= stringLength) {
        // Parse each digit from the string into integer values
        for (int i = 0; i < NO_OF_VAL_REC; i++) {
          int num = (i * DIGIT_PER_VAL_REC) + 1;  // Offset +1 to skip '$'
          valsRec[i] = receivedString.substring(num, num + DIGIT_PER_VAL_REC).toInt();
        }

        // Reset everything after data is fully read
        receivedString = "";
        counter = 0;
        counterStart = false;
      }
    }
  }
}
