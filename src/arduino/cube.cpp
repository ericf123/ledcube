#include "Arduino.h"

/*
 * This is a multiplexing driver for a 4x4x4 LED cube. Electrically, the cube is set up
 * as an 8x8 grid. The data sent by the computer over serial to set the state is arranged such that
 * every increment of 16bits represents an incremented x value. Every bit increment represents an 
 * increment in y, every 4 bit increment represents an increment in z. The most significant bit 
 * (LED 63) is stored in the 7th bit of state[7] (0-indexed). 
 * Pins 2-9 are the anodes of the LED cube, and pins 10-17 are the cathodes. 
 * Pins 13-17 are labeled as A0-A4 on the Arduino.
 */


byte state[8] = {0, 0, 0, 0, 0, 0, 0, 0};//store the state of all the LEDs, state[7] bit 7 is (4,4,4)
void display();

void setup() {
    //initialize pins 2-18 to outputs
    for (int i = 2; i < 18; i++){
        pinMode(i, OUTPUT);
        digitalWrite(i, HIGH);
    }
    Serial.begin(115200); //set the baudrate and open port
}

void loop(){
    //the CV controller won't send data if there is no change
   if (Serial.available() > 0){//read new data if it's available
        Serial.readBytes(state, 8);
    }
    display();//run one TDM cycle
}

void display(){
    for (int i = 2; i < 10; i++){//loop through anodes
        for (int j = 10; j < 18; j++){//loop through cathodes
            byte cathodeState = state[i-2] & (1 << (j-10));//use and to figure out if cathod j should be on
            //0 evaultes to false (LOW), so !0 will be true (HIGH)
            digitalWrite(j, !cathodeState);//writing low turns LED on
            if (cathodeState){
                Serial.print("a: ");
                Serial.print(i);
                Serial.print(", c: ");
                Serial.print(j);
            }
        }
        digitalWrite(i, LOW);//driver is a PMOS, so we need to write LOW to turn it on
        delayMicroseconds(100);
        digitalWrite(i, HIGH);//"turn off" anode
        Serial.println();
    } 
}
