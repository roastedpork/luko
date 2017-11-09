#ifndef SERVO_H
#define SERVO_H

// Joint 1 Parameters
// With analogin passing through 1k ohms 
#define J1_LOWER 0
#define J1_UPPER 180
#define J1_PIN   p20
#define J1_POUT  p21
#define J1_GRAD  0.00339
#define J1_INTC  0.13722

// Joint 2 Parameters
// With analogin passing through 1k ohms 
// analog conversion accurate in range [3,167]
#define J2_LOWER 47
#define J2_UPPER 94
#define J2_PIN   p19
#define J2_POUT  p22
#define J2_GRAD  0.00339
#define J2_INTC  0.170

// Joint 3 Parameters
// With analogin passing through 1k ohms 
// analog conversion accurate in range [5,160]
#define J3_LOWER 10
#define J3_UPPER 110
#define J3_PIN   p18
#define J3_POUT  p23
#define J3_GRAD  0.00328
#define J3_INTC  0.13036

// Joint 4 Parameters
// With analogin passing through 1k ohms 
// analog conversion accurate in range [5,160]
#define J4_LOWER 5
#define J4_UPPER 140
#define J4_PIN   p17
#define J4_POUT  p24
#define J4_GRAD  0.00324
#define J4_INTC  0.12868

// Joint 5 Parameters
// With analogin passing through 1k ohms 
// analog conversion accurate in range [1,168]
#define J5_LOWER 0
#define J5_UPPER 180
#define J5_PIN   p16
#define J5_POUT  p25
#define J5_GRAD  0.00343
#define J5_INTC  0.16594

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
