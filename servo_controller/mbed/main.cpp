#include <iostream>
#include <algorithm>

#include "mbed.h"

#include "geometry_msgs/Pose2D.h"

#include "constants.hpp"
#include "reader.hpp"

#define MSG_SIZE(x) (sizeof(x) - 8)

/* Peripherals */
Ticker ticker;
DigitalOut led1(LED1);
DigitalOut led2(LED2);
CAN can_bus(p30, p29);
Serial pc(USBTX, USBRX);

/* Data */
geometry_msgs::Pose2D pose;
eurobot::ReaderStateMachine<MSG_SIZE(geometry_msgs::Pose2D)> reader_sm;
geometry_msgs::Pose2D current_pose;
geometry_msgs::Pose2D target_pose;

static void
poll_can_bus_message()
{
  CANMessage msg;

  if (!can_bus.read(msg)) {
    return;
  }

  if (msg.id == eurobot::MOVE_TO_TARGET) {
    reader_sm.push(msg.data, msg.len);
  }

  if (reader_sm.done()) {
    /* UNSAFE cast here is intentional, because MBed's deserialization
     * routine is, inconveniently, written with non const arguments.
     * */
    target_pose.deserialize((unsigned char*) reader_sm.read_and_reset());
    pc.printf("Moving to (%.3f, %.3f, %.3f)\r\n",
        target_pose.x, target_pose.y, target_pose.theta);
  }
}

static void
broadcast_position()
{
  const uint32_t sz = MSG_SIZE(geometry_msgs::Pose2D);
  char buffer[sz];
  char *ptr = buffer;

  /* ROS uses [unsigned char] but mbed uses [char] */
  current_pose.serialize((unsigned char*) buffer);

  /* One would expect a good compiler to unroll this */
  uint32_t i = 0;
  while (i < sz) {
    uint32_t len = std::min(uint32_t(8u), sz - i);
    const char *cur = ptr;
    CANMessage msg = CANMessage(
        eurobot::ROBOT_CURRENT_POSITION,
        cur,
        len
    );

    if (can_bus.write(msg)) {
      i += 8;
      ptr += 8;
    } else {
      pc.printf("Position update failed at i = %u\r\n");
      break;
    }
  }
}

int main() {
  pc.baud(115200);
  can_bus.frequency(500000);
  pc.printf("Init - MSG_SIZE = %u\r\n", MSG_SIZE(geometry_msgs::Pose2D));

  ticker.attach(poll_can_bus_message, 1.0);
  ticker.attach(broadcast_position, 1.0);

  /* Control loop would come here */
  while (1) {
    current_pose.x = current_pose.x - 0.5 * (target_pose.x - current_pose.x);
    current_pose.y = current_pose.y - 0.5 * (target_pose.y - current_pose.y);
    current_pose.theta =
        current_pose.theta - 0.5 * (target_pose.theta - current_pose.theta);
    // pc.printf("Current position = (%.3f, %.3f, %.3f)\r\n",
    //     current_pose.x, current_pose.y, current_pose.theta);
    wait(1.0);
  }
}
