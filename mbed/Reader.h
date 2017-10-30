#ifndef READER_H
#define READER_H

// Reading 5 values in hex characters, encapsulated by '<' and '>'
// 

namespace SerialReader{
    extern RawSerial io;
    extern char bufferA[10];
    extern char bufferB[10];
    extern bool read_ready;
    extern uint8_t value[5];
    extern uint8_t write_ptr;
    
    extern void getValue();
    extern void addChar();
    extern void init();
}

#endif

