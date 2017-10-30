#include "mbed.h"
#include "Reader.h"
#include <stdlib.h>


namespace SerialReader{
    RawSerial io(p28,p27);
    char bufferA[10];
    char bufferB[10];
    static char writeto;
    static DigitalOut led2(LED2);
    static DigitalOut led3(LED3);
    static DigitalOut led4(LED4);

    uint8_t write_ptr;
    static bool write_flag;
    bool write_done;
    bool read_ready;
    uint8_t value[5];
    
    void getValue(){
        while(1){
            if(write_done){
                for(uint8_t i=0;i<5;i++){
                        char temp[2];
                        if(writeto=='A'){
                            temp[0] = bufferB[2*i];
                            temp[1] = bufferB[2*i+1];
                        
                        }else if(writeto=='B'){
                            temp[0] = bufferA[2*i];
                            temp[1] = bufferA[2*i+1]; 
                        }
                        value[i] = (uint8_t) std::strtol((const char*)&temp,NULL,16);
                }
                write_done = false;
                read_ready = true;
            }
        }
    }

    
    void addChar(){
        
        if (io.readable()){
            char c = io.getc();
            if(!write_flag && (c == '<')){ // start writing to buffer
                write_flag = true;
                write_ptr = 0;

            }else if(write_flag && (c == '>')){ //end writing to buffer
                write_flag = false;
                
                if(writeto=='A'){
                    writeto='B';
                }else if(writeto=='B'){
                    writeto='A';
                }
                
                write_done = true;
                write_ptr = 0;

            }else if(write_flag && (write_ptr == 10)){ // out of bounds error
                write_flag = false;
                write_ptr = 0;

            }else if(write_flag){ // write to buffer
                if(writeto=='A'){
                    bufferA[write_ptr++] = c;
                }else{
                    bufferB[write_ptr++] = c;
                }
            }
        }
    }
    
    void init(){
        io.baud(9600);
        io.attach(&addChar);
        std::memset(bufferA,0,10*sizeof(char));
        std::memset(bufferB,0,10*sizeof(char));
        std::memset(value,0,5*sizeof(uint8_t));
        writeto = 'A';
        
        write_ptr = 0;
        write_flag = false;
        write_done = false;
        read_ready = false;
        
        
    }
    
}

