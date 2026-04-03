#ifndef _CAN_INTERFACE_H
#define _CAN_INTERFACE_H

#include <inttypes.h>
#include <linux/can/raw.h>
class CanInterface
{
public:
  CanInterface() {}
  virtual ~CanInterface() {}
  virtual bool send_message(can_frame frame) = 0;
  virtual bool read_message(can_frame &frame) = 0;
  virtual bool available() = 0;
  virtual bool support_interrupt() = 0;
};

#endif  // CYBERGEAR_CAN_INTERFACE_HH