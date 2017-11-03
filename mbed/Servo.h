#ifndef SERVO_H
#define SERVO_H

// Joint 1 Parameters
#define J1_LOWER 0
#define J1_UPPER 180
#define J1_PIN   p20
#define J1_POUT  p21
#define J1_GRAD  0.00318
#define J1_INTC  0.126

// Joint 2 Parameters
#define J2_LOWER 0
#define J2_UPPER 180
#define J2_PIN   p19
#define J2_POUT  p22
#define J2_GRAD  0.00318
#define J2_INTC  0.126

// Joint 3 Parameters
#define J3_LOWER 0
#define J3_UPPER 180
#define J3_PIN   p18
#define J3_POUT  p23
#define J3_GRAD  0.00318
#define J3_INTC  0.126

// Joint 4 Parameters
#define J4_LOWER 0
#define J4_UPPER 180
#define J4_PIN   p17
#define J4_POUT  p24
#define J4_GRAD  0.00318
#define J4_INTC  0.126

// Joint 5 Parameters
#define J5_LOWER 0
#define J5_UPPER 180
#define J5_PIN   p16
#define J5_POUT  p25
#define J5_GRAD  0.00318
#define J5_INTC  0.126

// Servo Motion Resolution
#define STEP_TIME 50 // 50ms
#define STEP_VSLOW 2 // 2 degrees 
#define STEP_SLOW 3  // 3 degrees 
#define STEP_NORM 4  // 4 degrees
#define STEP_FAST 5  // 5 degrees

#include "mbed.h"

class Servo{
public:
    // Constructor/Destructor
    Servo(const uint8_t lower, const uint8_t upper,
            PinName ain, PinName pwmout,
            float grad, float intercept);
    ~Servo();
    
    // Servo Actuation methods
    void setAngle(const uint8_t angle);
    uint8_t getAngle();
    
    // Analog reading of servo voltage
    const float getAnalog();
    
    // Threaded implementation of servo actuation
    void setThreadParams(uint8_t target, int step = STEP_NORM);
    void setAngle_threaded();
    
    bool inMotion;
    
private:
    // Joint Limits
    uint8_t _lower;
    uint8_t _upper;
    
    // Servo Pins
    AnalogIn _ain;
    PwmOut _pwm;
    
    // Used for Linear conversion from analog value to angle reading
    float _grad;
    float _intercept;
    
    // Used for threaded running of motor
    uint8_t _target;
    int _step;
};


#endif
