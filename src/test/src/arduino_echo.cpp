#include "Arduino.h"

byte stateBuffer[8];
bool got_data = false;

void setup() {
    Serial.begin(115200);
}

void loop(){
    Serial.print(Serial.readBytes(stateBuffer, 8), DEC);
    Serial.print("\t");
    for (int i = 0; i < 8; i++){
        Serial.print(stateBuffer[i], DEC);
    }
    Serial.print("\n");
}
