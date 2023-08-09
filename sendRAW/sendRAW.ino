#include <Wire.h>
#include "MAX30105.h"



volatile int interruptCounter;
int totalInterruptCounter;
hw_timer_t * timer = NULL;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;


MAX30105 particleSensor;

float IR_val;
float Red_val;
bool siEnvia = false;

void IRAM_ATTR Adquiere()
{
  siEnvia = true;
}

void setup()
{
  Serial.begin(115200);
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }

  byte ledBrightness = 0x1F; //Options: 0=Off to 255=50mA
  byte sampleAverage = 8; //Options: 1, 2, 4, 8, 16, 32
  byte ledMode = 3; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  int sampleRate = 100; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411; //Options: 69, 118, 215, 411
  int adcRange = 4096; //Options: 2048, 4096, 8192, 16384

  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configure sensor with these settings

  
  const byte avgAmount = 64;
  long baseValue_IR = 0, baseValue_Red = 0;
  for (byte x = 0 ; x < avgAmount ; x++)
  {
    baseValue_IR += particleSensor.getIR();
    baseValue_Red += particleSensor.getRed();
    
  }
  baseValue_IR /= avgAmount;
  baseValue_Red /= avgAmount;
  
  for (int x = 0 ; x < 500 ; x++)
  {
    Serial.print(baseValue_IR);
    Serial.print(", ");
    Serial.println(baseValue_Red);
  }
  
  particleSensor.enableDATARDY();
  
  timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timer, &Adquiere, true);
  timerAlarmWrite(timer, 1000000/100, true);
  timerAlarmEnable(timer);
}


void loop()
{
  if(siEnvia)
  {
    IR_val = particleSensor.getIR();
    //Red_val = particleSensor.getRed();
    Serial.println(IR_val);
    //Serial.print(", ");
    //Serial.println(Red_val);
    siEnvia = false;
  }
}