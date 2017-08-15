const byte ANODE_PINS[8] = {2, 3, 4, 5, 6, 7, 8, 9};
const byte CATHODE_PINS[8] = {10, 11, 12, 13, A3, A2, A1, A0};
bool cleared;
void setup()
{
    // Make all of the anode (+) wire and cathode (-) wire pins outputs
    for (byte i = 0; i < 8; i++) {
        pinMode(ANODE_PINS[i], OUTPUT);
        pinMode(CATHODE_PINS[i], OUTPUT);
        //initialize everything to off
        digitalWrite(ANODE_PINS[i], HIGH);
        digitalWrite(CATHODE_PINS[i], HIGH);
    }

    // Initialize serial communication
    Serial.begin(115200);
    cleared = false;
}

/* Function: getLEDState
   ---------------------
   Returns the state of the LED in a 4x4x4 pattern array, each dimension
   representing an axis of the LED cube, that corresponds to the given anode (+)
   wire and cathode (-) wire number.
 */
inline byte getLEDState(byte pattern[4][4][4], byte aNum, byte cNum)
{
    /*
        This is a formula I derived by basically thinking for awhile. 
        The reason it needs absolute value is because for the z=1 plane,
        the result returned is actually -1, so we use absolute value to correct
        this.
    */
    byte z = abs(2 * (aNum / 4) + (aNum / 4 - cNum / 4));
    return pattern[aNum % 4][cNum % 4][z];
}

/* Function: display
   -----------------
   Runs through one multiplexing cycle of the LEDs, controlling which LEDs are
   on.

   During this function, LEDs that should be on will be turned on momentarily,
   one row at a time. When this function returns, all the LEDs will be off
   again, so it needs to be called continuously for LEDs to be on.
 */
void display(byte pattern[4][4][4])
{
    for (byte aNum = 0; aNum < 8; aNum++) { // iterate through anode (+) wires
        // Set up all the cathode (-) wires first
        for (byte cNum = 0; cNum < 8; cNum++) { // iterate through cathode (-) wires
            byte value = getLEDState(pattern, aNum, cNum); // look up the value
            digitalWrite(CATHODE_PINS[cNum], !value);
        }

        //turn anode, wait, turn off
        digitalWrite(ANODE_PINS[aNum], LOW);//set PMOS gate LOW, so anode is high
        delayMicroseconds(100);
        digitalWrite(ANODE_PINS[aNum], HIGH);
    }
}

/*
    Function: decodeState
    ---------------------
    Here we decode the state sent over serial as 8 bytes and update the pattern
    accordingly.

*/
void decodeState(byte encodedState[8], byte pattern[4][4][4]) {
    //for a detailed explanation of the encoding used, see the cubestate.py file in src/controller.
    for (int i = 0; i < 8; i++) {//loop through bytes
        for (int j = 0; j < 8; j++) {//loop through bits
            //first we determine which position we are setting
            byte x = i / 2;
            byte y = j % 4;
            byte z = 2 * (i % 2) + (j / 4);
            //then we figure out the state of this position
            pattern[x][y][z] = encodedState[i] & (1 << j);
        }
    }
}

/*
   Below method is for question L1. It is
   inentionally unused.
 */

void loopThroughAll() {
    for (byte aNum = 0; aNum < 8; aNum++) { // iterate through anode (+) wires
        digitalWrite(ANODE_PINS[aNum], LOW);//set PMOS gate LOW, so anode is high
        for (byte cNum = 0; cNum < 8; cNum++) { // iterate through cathode (-) wires
            digitalWrite(CATHODE_PINS[cNum], LOW);
            delayMicroseconds(100);
            digitalWrite(CATHODE_PINS[cNum], HIGH);
        }
        digitalWrite(ANODE_PINS[aNum], HIGH);
    }
}

void loop() {
    static byte ledPattern[4][4][4]; // 1 for on, 0 for off
    if (Serial.available() > 0) {//if the controller is sending data, read it
        byte encodedState[8];
        Serial.readBytes(encodedState, 8);
        decodeState(encodedState, ledPattern);//write data to a format we can work with
    }

    display(ledPattern);//run one TDM cycle
}
