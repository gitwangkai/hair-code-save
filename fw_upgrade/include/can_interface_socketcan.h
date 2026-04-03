#ifndef __ros2_socketcan_H__
#define __ros2_socketcan_H__

#include "can_interface.h"
#include "iostream"
#include <boost/asio.hpp>
#include <deque>
#include <linux/can/raw.h>
#include <stdlib.h>

class SocketcanInterface : public CanInterface {
public:
  /**
   * @brief constructor for socketcan class
   * @details Within the constructor the topic and service naming is done.
   */
  SocketcanInterface(
      std::string can_socket_interface = "can0",
      int can_bitrate = 500000); // boost::asio::io_service& ios);

  void Init();
  virtual bool send_message(can_frame frame);
  virtual bool read_message(can_frame &frame);
  virtual bool available();
  virtual bool support_interrupt();
  /**
   * @brief destructor
   */
  ~SocketcanInterface();

private:
  /**
   * @brief The CanSendConfirm function is needed by the .async_write_some
   * function and is called as confirmation for a successfull send process.
   */
  void CanSendConfirm();

  void CanSend(can_frame frame);

  void CanListener(struct can_frame &rec_frame,
                   boost::asio::posix::basic_stream_descriptor<> &stream);

  /**
   * @biref The Stop method is needed as the interuped handler must be
   * configered to the asio libary.
   */
  void stop();

  boost::asio::io_service ios;
  boost::asio::posix::basic_stream_descriptor<> stream;
  boost::asio::signal_set signals;

  struct sockaddr_can addr;
  struct can_frame frame;
  struct can_frame rec_frame;
  struct ifreq ifr;

  int natsock = socket(PF_CAN, SOCK_RAW, CAN_RAW);
  std::stringstream topicname_receive;
  std::stringstream topicname_transmit;
  std::stringstream servername;
  int can_bitrate_ = 1000000;
  std::string can_socket_interface_;
  std::mutex mu_dq;
  std::deque<can_frame> receive_buffer_;
};
#endif