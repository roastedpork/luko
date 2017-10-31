#include "Servo.h"
#include <math.h>

Servo::Servo(const uint8_t lower, const uint8_t upper,
        PinName ain, PinName pwmout)
        : _lower(lower), _upper(upper), 
        _ain(AnalogIn(ain)), _pwm(PwmOut(pwmout)){
            _pwm.period(0.020);
            _pwm.write(0.0);            
}

Servo::~Servo(){};

void Servo::setAngle(const uint8_t angle){
    if ((_lower <= angle) && (angle <= _upper)){
        float width = ((float)angle/180.0)*2000 + 500;
        _pwm.pulsewidth_us((int) floor(width+0.5));
    }
}

const float Servo::getAnalog(){
    return _ain;
}

uint8_t Servo::getAngle(){
    return 180.0 * _ain;
}
