#ifndef READER_H
#define READER_H

#include <stdint.h>

namespace eurobot
{

template <uint32_t N>
class ReaderStateMachine {
private:
  uint8_t data[N];
  uint32_t counter;

public:
  ReaderStateMachine() {}

  const bool done() const
  {
    return (counter >= N - 1);
  }

  const void push(const uint8_t *p, uint32_t len)
  {
    memcpy(data + counter, p, len);
    counter += len;
  }

  const unsigned char* read_and_reset()
  {
    counter = 0;
    return data;
  }
};

}

#endif
