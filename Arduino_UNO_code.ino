#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif
#include <HX711_ADC.h>

//Function declaration
void calibrate();


void changeSavedCalFactor();


//pins:
const int HX711_sck = 5;                                 //mcu > HX711 dout pin
const int HX711_dout_1 = 4;                                  //mcu > HX711 sck pin
const int HX711_dout_2 = 6;
const int HX711_dout_3 = 9;                                  //mcu > HX711 sck pin

//HX711 constructor:
HX711_ADC LoadCell_1(HX711_dout_1, HX711_sck);
HX711_ADC LoadCell_2(HX711_dout_2, HX711_sck);
HX711_ADC LoadCell_3(HX711_dout_3, HX711_sck);


const int calVal_eepromAdress = 0;
unsigned long t = 0;
int diff = 10;
int iterasjon = 0;
const int h = 10;
bool printFeil;

int dataSpeed = 9600;

float vals1[h];
float vals2[h];
float vals3[h];

float sum1 = 0;
float sum2 = 0;
float sum3 = 0;

float avg1;
float avg2;
float avg3;
      



void setup() {
  Serial.begin(dataSpeed); 
  delay(10);
  //Serial.println();
  //Serial.println("Starting...");

  LoadCell_1.begin();
  LoadCell_2.begin();
  LoadCell_3.begin();

  float calibrationValue_1;                                   // calibration value (see example file "Calibration.ino")
  calibrationValue_1 = -251; //696.0;                                 // uncomment this if you want to set the calibration value in the sketch
  float calibrationValue_2;                                   // calibration value (see example file "Calibration.ino")
  calibrationValue_2 = 201; 
  float calibrationValue_3;                                   // calibration value (see example file "Calibration.ino")
  calibrationValue_3 = 100.0; 
#if defined(ESP8266)|| defined(ESP32)

  //EEPROM.begin(512);                                      // uncomment this if you use ESP8266/ESP32 and want to fetch the calibration value from eeprom
#endif
  //EEPROM.get(calVal_eepromAdress, calibrationValue);        // uncomment this if you want to fetch the calibration value from eeprom

  unsigned long stabilizingtime = 2000;                     // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true;                                     //set this to false if you don't want tare to be performed in the next step
  LoadCell_1.start(stabilizingtime, _tare);
  LoadCell_2.start(stabilizingtime, _tare);
  LoadCell_3.start(stabilizingtime, _tare);

  
  if (LoadCell_1.getTareTimeoutFlag() || LoadCell_1.getSignalTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell_1.setCalFactor(calibrationValue_1);             // set calibration value (float)
    Serial.println("Startup is complete");
  }

  if (LoadCell_2.getTareTimeoutFlag() || LoadCell_2.getSignalTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell_2.setCalFactor(calibrationValue_2);             // set calibration value (float)
    Serial.println("Startup is complete");
  }

  if (LoadCell_3.getTareTimeoutFlag() || LoadCell_3.getSignalTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell_3.setCalFactor(calibrationValue_3);             // set calibration value (float)
    Serial.println("Startup is complete");
  }
  for (int n = 0; n < h; n++){
        vals1[n] = 0;
        vals2[n] = 0;
        vals3[n] = 0;
  }
  
  /*
  while (!LoadCell_1.update());
  calibrate();                                            //start calibration procedure
}
*/
                                                                                                                                                      /*__________________________________________*/
}


void loop() {

  static boolean newDataReady_1 = 0;
  static boolean newDataReady_2 = 0;
  static boolean newDataReady_3 = 0;
  const int serialPrintInterval = 1000;                     //increase value to slow down serial print activity
                                                         
  if (LoadCell_1.update()) newDataReady_1 = true;               // check for new data/start next conversion:       
  if (LoadCell_2.update()) newDataReady_2 = true;               // check for new data/start next conversion:                                                      
  if (LoadCell_3.update()) newDataReady_3 = true;               // check for new data/start next conversion:                                                      

                                             
  
  if (newDataReady_1 and newDataReady_2 and newDataReady_3) {                                       // get smoothed value from the dataset:
    if (millis() > t + serialPrintInterval) {
      float i = LoadCell_1.getData();
      if(String(i) == "inf"){
        Serial.print("Error ");
        Serial.println(25);
      }
      else if(String(i) == "nan"){
         Serial.print("Error ");
        Serial.println(42);
      }
      else{
      //Serial.print("Load_cell_1 output val: ");
      //Serial.println(i);
      }      

      
      float j = LoadCell_2.getData();
      if(String(j) == "inf"){
        Serial.print("Error ");
        Serial.println(25);
      }
      else if(String(j) == "nan"){
         Serial.print("Error ");
        Serial.println(42);
      }
      else{
      //Serial.print("Load_cell_2 output val: ");
      //Serial.println(j);
      }      


      float l = LoadCell_3.getData();
      if(String(l) == "inf"){
        Serial.print("Error ");
        Serial.println(25);
      }
      else if(String(l) == "nan"){
         Serial.print("Error ");
        Serial.println(42);
      }
      else{
      //Serial.print("Load_cell_3 output val: ");
      //Serial.println(l);
      }      

      newDataReady_1 = 0;
      newDataReady_2 = 0;
      newDataReady_3 = 0;
      
      sum1 = 0;
      sum2 = 0;
      sum3 = 0;
      
      t = millis();
      
      for (int n = h-1; n > 0; n--){
        vals1[n] = vals1[n-1];   
        vals2[n] = vals2[n-1];
        vals3[n] = vals3[n-1];

        //Serial.println(vals1[n]);
        //Serial.println(vals2[n]);
        //Serial.println(vals3[n]);
        
        sum1 += vals1[n];
        sum2 += vals2[n];
        sum3 += vals3[n];
      }


      vals1[0] = i;   
      vals2[0] = j;
      vals3[0] = l;

      sum1 += vals1[0];
      sum2 += vals2[0];
      sum3 += vals3[0];

      avg1 = sum1/h;
      avg2 = sum2/h;
      avg3 = sum3/h;

      Serial.print("data")
      Serial.print("0 ");
      Serial.println(avg1);

      Serial.print("data")
      Serial.print("1 ");
      Serial.println(avg2);

      Serial.print("data")
      Serial.print("2 ");
      Serial.println(avg3);

      }
    }


                                                        
  if (Serial.available() > 0) {                             //receive command from serial terminal, send 't' to initiate tare operation:
    char inByte = Serial.read();
    if (inByte == 't') {LoadCell_1.tareNoDelay();}          //tare
    else if (inByte == 'x') printFeil = false;              //stillhet
    else if (inByte == 'r') calibrate();                      
    else if (inByte == 'c') changeSavedCalFactor();         //edit calibration value manually
   }

  
  if (LoadCell_1.getTareStatus() == true) {                 // check if last tare operation is complete:
    Serial.println("Tare 1 complete");
  }
  if (LoadCell_2.getTareStatus() == true) {                 // check if last tare operation is complete:
    Serial.println("Tare 2 complete");
  }
  if (LoadCell_3.getTareStatus() == true) {                 // check if last tare operation is complete:
    Serial.println("Tare 3 complete");
  }
}
                                                                                                                                  /*--------Function Definisjon----------*/


                                                        
                                                        

void calibrate() {
  Serial.println("***");
  Serial.println("Start calibration:");
  Serial.println("Place the load cell an a level stable surface.");
  Serial.println("Remove any load applied to the load cell.");
  Serial.println("Send 't' from serial monitor to set the tare offset.");

  boolean _resume = false;
  while (_resume == false) {
    LoadCell_2.update();
    if (Serial.available() > 0) {
      if (Serial.available() > 0) {
        char inByte = Serial.read();
        if (inByte == 't') LoadCell_2.tareNoDelay();
      }
    }
    if (LoadCell_2.getTareStatus() == true) {
      Serial.println("Tare complete");
      _resume = true;
    }
  }

  Serial.println("Now, place your known mass on the LoadCell_1.");
  Serial.println("Then send the weight of this mass (i.e. 100.0) from serial monitor.");

  float known_mass = 0;
  _resume = false;
  while (_resume == false) {
    LoadCell_2.update();
    if (Serial.available() > 0) {
      known_mass = Serial.parseFloat();
      if (known_mass != 0) {
        Serial.print("Known mass is: ");
        Serial.println(known_mass);
        _resume = true;
      }
    }
  }

  LoadCell_2.refreshDataSet(); //refresh the dataset to be sure that the known mass is measured correct
  float newCalibrationValue = LoadCell_2.getNewCalibration(known_mass); //get the new calibration value

  Serial.print("New calibration value has been set to: ");
  Serial.print(newCalibrationValue);
  Serial.println(", use this as calibration value (calFactor) in your project sketch.");
  Serial.print("Save this value to EEPROM adress ");
  Serial.print(calVal_eepromAdress);
  Serial.println("? y/n");

  _resume = false;
  while (_resume == false) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.begin(512);
#endif
        EEPROM.put(calVal_eepromAdress, newCalibrationValue);
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.commit();
#endif
        EEPROM.get(calVal_eepromAdress, newCalibrationValue);
        Serial.print("Value ");
        Serial.print(newCalibrationValue);
        Serial.print(" saved to EEPROM address: ");
        Serial.println(calVal_eepromAdress);
        _resume = true;

      }
      else if (inByte == 'n') {
        Serial.println("Value not saved to EEPROM");
        _resume = true;
      }
    }
  }

  Serial.println("End calibration");
  Serial.println("***");
  Serial.println("To re-calibrate, send 'r' from serial monitor.");
  Serial.println("For manual edit of the calibration value, send 'c' from serial monitor.");
  Serial.println("***");
}

                                                     


void changeSavedCalFactor() {
  float oldCalibrationValue = LoadCell_1.getCalFactor();
  boolean _resume = false;
  Serial.println("***");
  Serial.print("Current value is: ");
  Serial.println(oldCalibrationValue);
  Serial.println("Now, send the new value from serial monitor, i.e. 696.0");
  float newCalibrationValue;
  while (_resume == false) {
    if (Serial.available() > 0) {
      newCalibrationValue = Serial.parseFloat();
      if (newCalibrationValue != 0) {
        Serial.print("New calibration value is: ");
        Serial.println(newCalibrationValue);
        LoadCell_3.setCalFactor(newCalibrationValue);
        _resume = true;
      }
    }
  }
  _resume = false;
  Serial.print("Save this value to EEPROM adress ");
  Serial.print(calVal_eepromAdress);
  Serial.println("? y/n");
  while (_resume == false) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.begin(512);
#endif
        EEPROM.put(calVal_eepromAdress, newCalibrationValue);
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.commit();
#endif
        EEPROM.get(calVal_eepromAdress, newCalibrationValue);
        Serial.print("Value ");
        Serial.print(newCalibrationValue);
        Serial.print(" saved to EEPROM address: ");
        Serial.println(calVal_eepromAdress);
        _resume = true;
      }
      else if (inByte == 'n') {
        Serial.println("Value not saved to EEPROM");
        _resume = true;
      }
    }
  }
  Serial.println("End change calibration value");
  Serial.println("***");
}
