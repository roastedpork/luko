#include "Servo.h"
#include "mbed.h"
#include "rtos.h"
#include <math.h>



Servo::Servo(const uint8_t lower, const uint8_t upper,
        PinName ain, PinName pwmout, 
        float grad, float intercept)
        : _lower(lower), _upper(upper), 
        _ain(AnalogIn(ain)), _pwm(PwmOut(pwmout)),
        _grad(grad), _intercept(intercept), inMotion(false){
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

void Servo::setThreadParams(uint8_t target, int step){
    _target = target;
    _step = step; 
}

void Servo::setAngle_threaded(){
        int current = getAngle();
        int traverse = ((int)_target)-current;
        
        inMotion = true;
        while (traverse){
            if (traverse >= _step) current += _step;
            else if (traverse <= -_step) current -= _step;
            else current = _target;
            
            traverse = _target-current;
            setAngle(current);
            Thread::wait(STEP_TIME);
        }
        inMotion = false;
}

const float Servo::getAnalog(){
    return _ain;
}

uint8_t Servo::getAngle(){
    return floor((_ain-_intercept)/_grad + 0.5)-3;
}
