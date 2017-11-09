/*
 * rosserial Servo Control Example
 *
 * This sketch demonstrates the control of hobby R/C servos
 * using ROS and an MBED board
 *
 */

#include "mbed.h"
#include "rtos.h"
#include "Servo.h"
#include "Reader.h"

#include <stdlib.h>
#include <time.h>

uint8_t tgt_joints[5]={1,2,3,4,5};
uint8_t cur_joints[5]={1,2,3,4,5};

Servo joints[5] =   {
                    Servo(J1_LOWER,J1_UPPER,J1_PIN,J1_POUT,J1_GRAD,J1_INTC),
                    Servo(J2_LOWER,J2_UPPER,J2_PIN,J2_POUT,J2_GRAD,J2_INTC),
                    Servo(J3_LOWER,J3_UPPER,J3_PIN,J3_POUT,J3_GRAD,J3_INTC),
                    Servo(J4_LOWER,J4_UPPER,J4_PIN,J4_POUT,J4_GRAD,J4_INTC),
                    Servo(J5_LOWER,J5_UPPER,J5_PIN,J5_POUT,J5_GRAD,J5_INTC)
                    };
                  
Serial pc(USBTX,USBRX);
DigitalOut myled(LED1);
Thread serial_thread(osPriorityNormal, 850);
Thread mthreads[5] = {  Thread(osPriorityNormal, 200),
                        Thread(osPriorityNormal, 200),
                        Thread(osPriorityNormal, 200),
                        Thread(osPriorityNormal, 200),
                        Thread(osPriorityNormal, 200) };
                        
int main() {

    pc.baud(9600);
    SerialReader::init();
    serial_thread.start(SerialReader::getValue);
    myled = 1;


//    const int start = 45;
//    const int end = 5;    
//    joints[0].setAngle(90);
//    joints[1].setAngle(start);
//    joints[2].setAngle(20);
//    joints[3].setAngle(90);
    joints[4].setAngle(90);
//    wait_ms(1500);


//    joints[0].setThreadParams(end,STEP_FAST);
//    joints[1].setThreadParams(end,STEP_FAST);
//    joints[2].setThreadParams(end,STEP_FAST);
//    mthreads[0].start(&joints[0],&Servo::setAngle_threaded);
//    mthreads[1].start(&joints[1],&Servo::setAngle_threaded);
//    mthreads[2].start(&joints[2],&Servo::setAngle_threaded);
//    mthreads[3].start(&joints[3],&Servo::setAngle_threaded);
//    mthreads[4].start(&joints[4],&Servo::setAngle_threaded);
    
//    pc.printf("[0] Total: %d, Free: %d, Used: %d\n\r", mthreads[0].stack_size(),mthreads[0].free_stack(),mthreads[0].used_stack());
//    pc.printf("[1] Total: %d, Free: %d, Used: %d\n\r", mthreads[1].stack_size(),mthreads[1].free_stack(),mthreads[1].used_stack());
//    pc.printf("[2] Total: %d, Free: %d, Used: %d\n\r", mthreads[2].stack_size(),mthreads[2].free_stack(),mthreads[2].used_stack());
//    pc.printf("[3] Total: %d, Free: %d, Used: %d\n\r", mthreads[3].stack_size(),mthreads[3].free_stack(),mthreads[3].used_stack());
//    pc.printf("[4] Total: %d, Free: %d, Used: %d\n\r", mthreads[4].stack_size(),mthreads[4].free_stack(),mthreads[4].used_stack());

    while(1){
        

        if (SerialReader::read_ready){
            myled = !myled;
            std::memcpy(tgt_joints,SerialReader::value,5*sizeof(uint8_t));
            SerialReader::read_ready = false;
            for(unsigned i = 0;i<5;i++){
                if (joints[i].inMotion) mthreads[i].terminate();
                joints[i].setThreadParams(tgt_joints[i], STEP_FAST);
                mthreads[i].start(&joints[i],&Servo::setAngle_threaded);
            }
        }
        
        for(unsigned i=0; i<5; i++) cur_joints[i] = joints[i].getAngle();
        
        pc.printf("now:<%02x%02x%02x%02x%02x>\n\r",
                    cur_joints[0],cur_joints[1],cur_joints[2],
                    cur_joints[3],cur_joints[4]);
        SerialReader::io.printf("now:<%02x%02x%02x%02x%02x>\n\r",
                    cur_joints[0],cur_joints[1],cur_joints[2],
                    cur_joints[3],cur_joints[4]);
        wait_ms(100);
    }  

        // Calibration round 1 (angle vs analog readout)
//        int start = 120;
//        joints[4].setAngle(start);
//        wait_ms(2000);
//        
//        for(int target = start;target<=start+60;target++){
//
//                joints[4].setAngle(target);
//                wait_ms(50);
//                
//                float actual = joints[4].getAnalog();
//            
//                
//                pc.printf("Target, %03d, actual, %0.06f\r\n", target, actual);
//        }
  
    
        // calibration round 2 (angle vs processed)
//        int start = 0;
//        joints[4].setAngle(start);
//        wait_ms(1000);
//
//        for(int target = start;target<=start+ 60;target++){
//
//                joints[4].setAngle(target);
//                wait_ms(50);
//                
//                int actual = joints[4].getAngle();
//            
//                
//                pc.printf("Target, %03d, diff, %d\r\n", target, actual-target);
//        }

        // calibration round 3 (angle vs processed on frame)
//        joints[4].setAngle(0);
//        wait_ms(2000);
//
//        for(int target = 0;target<=180;target++){
//
//                joints[4].setAngle(target);
//                wait_ms(50);
//                
//                int actual = joints[4].getAngle();
//            
//                
//                pc.printf("Target, %03d, diff, %d\r\n", target, actual-target);
//        }
  
        
  
        return 0;
}


