#include "mbed.h"
#include "rtos.h"
#include "Servo.h"
#include "Reader.h"


uint8_t tgt_joints[5]={1,2,3,4,5};
uint8_t cur_joints[5]={1,2,3,4,5};

Servo joints[5] =   {
                    Servo(J1_LOWER,J1_UPPER,J1_PIN,J1_POUT),
                    Servo(J2_LOWER,J2_UPPER,J2_PIN,J2_POUT),
                    Servo(J3_LOWER,J3_UPPER,J3_PIN,J3_POUT),
                    Servo(J4_LOWER,J4_UPPER,J4_PIN,J4_POUT),
                    Servo(J5_LOWER,J5_UPPER,J5_PIN,J5_POUT)
                    };
                  
Serial pc(USBTX,USBRX);
DigitalOut myled(LED1);
Thread serial_thread(osPriorityNormal, 850);

int main() {
/*
    SerialReader::init();
    serial_thread.start(SerialReader::getValue);
    myled = 1;
    
    
    while(1){
        myled = !myled;

        if (SerialReader::read_ready){
            std::memcpy(tgt_joints,SerialReader::value,5*sizeof(uint8_t));
            SerialReader::read_ready = false;
        }

        for(uint8_t i=0;i<5;i++){
                if(cur_joints[i] > tgt_joints[i]) cur_joints[i]--;
                if(cur_joints[i] < tgt_joints[i]) cur_joints[i]++;
        }

        SerialReader::io.printf("tgt:<%02x%02x%02x%02x%02x>\n\r",
                    tgt_joints[0],tgt_joints[1],tgt_joints[2],
                    tgt_joints[3],tgt_joints[4]);
        SerialReader::io.printf("now:<%02x%02x%02x%02x%02x>\n\r",
                    cur_joints[0],cur_joints[1],cur_joints[2],
                    cur_joints[3],cur_joints[4]);

        wait_ms(500);
    }  
*/
        pc.baud(9600);

        joints[0].setAngle(45);
        wait_ms(1000);
        joints[0].setAngle(90);
        wait_ms(1000);
        joints[0].setAngle(135);
        wait_ms(1000);
        return 0;
}


