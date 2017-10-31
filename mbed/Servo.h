#ifndef SERVO_H
#define SERVO_H

#define J1_LOWER 0
#define J1_UPPER 180
#define J1_PIN   p20
#define J1_POUT  p21

#define J2_LOWER 0
#define J2_UPPER 180
#define J2_PIN   p19
#define J2_POUT  p22

#define J3_LOWER 0
#define J3_UPPER 180
#define J3_PIN   p18
#define J3_POUT  p23

#define J4_LOWER 0
#define J4_UPPER 180
#define J4_PIN   p17
#define J4_POUT  p24

#define J5_LOWER 0
#define J5_UPPER 180
#define J5_PIN   p16
#define J5_POUT  p25

#include "mbed.h"

class Servo{
public:
    Servo(const uint8_t lower, const uint8_t upper,
            PinName ain, PinName pwmout);
    ~Servo();
    void setAngle(const uint8_t angle);
    const float getAnalog();
    uint8_t getAngle();

private:
    uint8_t _lower, _upper;
    AnalogIn _ain;
    PwmOut _pwm;
};


#endif
