#include "Arduino.h"

byte stateBuffer[8];
void display();
void setup() {
    //initialize pins 2-18 to outputs
    for (int i = 2; i < 18; i++){
        pinMode(i, OUTPUT);
    }
    /*pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(7, OUTPUT);
    pinMode(8, OUTPUT);
    pinMode(9, OUTPUT);
    pinMode(10, OUTPUT);
    pinMode(11, OUTPUT);
    pinMode(12, OUTPUT);
    pinMode(13, OUTPUT);
    pinMode(14, OUTPUT);
    pinMode(15, OUTPUT);
    pinMode(16, OUTPUT);
    pinMode(17, OUTPUT);*/
    Serial.begin(115200);
}

void loop(){
    if (Serial.available() > 0){//read new data if it's available
        Serial.readBytes(stateBuffer, 8);
    }
    /*for (int i = 7; i >= 0; i--){
        Serial.print(stateBuffer[2]);
    }*/
    display();
}

void display(){
    for (int i = 2; i < 10; i++){//loop through anodes
        digitalWrite(i, HIGH);
        for (int j = 10; j < 18; j++){//loop through cathodes
            digitalWrite(j, !(stateBuffer[i-2] & (1 << (j - 10))));//writing low turns LED on
        }
        digitalWrite(i, LOW);
    } 
}
