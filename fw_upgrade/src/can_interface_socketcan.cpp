#include "can_interface_socketcan.h"

/**
 * @brief SocketcanInterface的构造函数
 *
 * 初始化SocketcanInterface对象，并设置CAN套接字接口和比特率。
 *
 * @param can_socket_interface CAN套接字接口的名称
 * @param can_bitrate CAN总线的比特率
 */
SocketcanInterface::SocketcanInterface(std::string can_socket_interface,
                                       int can_bitrate)
    : can_socket_interface_(can_socket_interface), can_bitrate_(can_bitrate),
      stream(ios), signals(ios, SIGINT, SIGTERM) {}

/**
 * @brief 初始化 SocketCAN 接口
 *
 * 该函数用于初始化 SocketCAN
 * 接口，包括设置比特率、启用或禁用接口以及绑定套接字。
 *
 * @return 无返回值
 */
void SocketcanInterface::Init() {

  std::string interface(can_socket_interface_);
/*
  std::string bringDownCmd = "sudo ip link set down " + interface;
  int result = system(bringDownCmd.c_str());
  if (result != 0) {
    std::cerr << "Failed to bring down " << interface << std::endl;
    return;
  }

  std::string setBitrateCmd = "sudo ip link set " + interface +
                              " type can bitrate " +
                              std::to_string(can_bitrate_);
  result = system(setBitrateCmd.c_str());
  if (result != 0) {
    std::cerr << "Failed to set bitrate for " << interface << std::endl;
    return;
  }

  std::string bringUpCmd = "sudo ip link set up " + interface;

  result = system(bringUpCmd.c_str());
  if (result != 0) {
    std::cerr << "Failed to bring up " << interface << std::endl;
    return;
  }
*/
  topicname_receive << "CAN/" << interface << "/" << "receive";
  topicname_transmit << "CAN/" << interface << "/" << "transmit";

  strcpy(ifr.ifr_name, interface.c_str());
  ioctl(natsock, SIOCGIFINDEX, &ifr);

  addr.can_family = AF_CAN;
  addr.can_ifindex = ifr.ifr_ifindex;

  if (bind(natsock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    perror("Error in socket bind");
  }

  stream.assign(natsock);

  stream.async_read_some(boost::asio::buffer(&rec_frame, sizeof(rec_frame)),
                         std::bind(&SocketcanInterface::CanListener, this,
                                   std::ref(rec_frame), std::ref(stream)));

  signals.async_wait(std::bind(&SocketcanInterface::stop, this));

  boost::system::error_code ec;

  std::size_t (boost::asio::io_service::*run)() = &boost::asio::io_service::run;
  std::thread bt(std::bind(run, &ios));
  bt.detach();
}

/**
 * @brief 停止 SocketcanInterface
 *
 * 该函数用于停止
 * SocketcanInterface，并在控制台上打印提示信息，指示监听线程已结束，
 * 提示用户再次按下 strg+c 以停止整个程序。
 *
 * @note 该函数会调用 ios.stop() 停止输入输出流，并清空 signals 信号集合。
 */
void SocketcanInterface::stop() {
  printf(
      "\nEnd of Listener Thread. Please press strg+c again to stop the whole "
      "program.\n");
  ios.stop();
  signals.clear();
}

SocketcanInterface::~SocketcanInterface() { printf("\nEnd of Thread. \n"); }

/**
 * @brief 发送CAN帧
 *
 * 该函数用于通过SocketCAN接口发送一个CAN帧。首先，它会打印出CAN帧的ID和数据内容，
 * 然后使用异步方式通过Boost.Asio库将CAN帧写入到网络流中。
 *
 * @param frame 要发送的CAN帧
 */
void SocketcanInterface::CanSend(can_frame frame) {

  // printf("S | %x | %s | ", frame.can_id, frame.data);
  // for (int j = 0; j < (int)frame.can_dlc; j++) {
  //   printf("%x ", frame.data[j]);
  // }
  // printf("\n");

  stream.async_write_some(boost::asio::buffer(&frame, sizeof(frame)),
                          std::bind(&SocketcanInterface::CanSendConfirm, this));
}

void SocketcanInterface::CanSendConfirm(void) {
  // std::cout << "Message sent" << std::endl;
}

/**
 * @brief SocketcanInterface类的CanListener成员函数
 *
 * 该函数是一个回调函数，用于监听并处理CAN帧数据。
 *
 * @param rec_frame CAN帧结构体引用，包含接收到的CAN帧数据
 * @param stream
 * boost::asio::posix::basic_stream_descriptor<>的引用，用于异步读取CAN帧数据
 */
void SocketcanInterface::CanListener(
    struct can_frame &rec_frame,
    boost::asio::posix::basic_stream_descriptor<> &stream) {

  std::stringstream s;

  // printf("R | %x | ", rec_frame.can_id);
  // for (int i = 0; i < rec_frame.can_dlc; i++) {
  //   s << rec_frame.data[i];
  // }

  // std::cout << s.str() << " | ";

  // for (int j = 0; j < (int)rec_frame.can_dlc; j++) {
  //   printf("%x ", rec_frame.data[j]);
  // }
  // printf("\n");

  {
    std::lock_guard<std::mutex> lock(mu_dq);
    receive_buffer_.push_back(rec_frame);
    if (receive_buffer_.size() > 1000) {
      receive_buffer_.pop_front();
    }
  }

  stream.async_read_some(boost::asio::buffer(&rec_frame, sizeof(rec_frame)),
                         std::bind(&SocketcanInterface::CanListener, this,
                                   std::ref(rec_frame), std::ref(stream)));
}
bool SocketcanInterface::send_message(can_frame frame) {
  CanSend(frame);
  return true;
}
/**
 * @brief 从接收缓冲区中读取一条消息
 *
 * 从接收缓冲区中读取一条消息，并将其存储在传入的 can_frame 类型的引用参数中。
 * 如果接收缓冲区为空，则返回 false；否则，将缓冲区中的第一条消息取出并存储在
 * frame 中， 同时从缓冲区中移除该消息，并返回 true。
 *
 * @param frame 存储读取到的消息的 can_frame 类型引用参数
 *
 * @return 如果成功读取到消息，则返回 true；否则返回 false
 */
bool SocketcanInterface::read_message(can_frame &frame) {
  std::lock_guard<std::mutex> lock(mu_dq);
  if (receive_buffer_.empty()) {
    return false;
  } else {
    frame = receive_buffer_.front();
    receive_buffer_.pop_front();
  }
  return true;
}
bool SocketcanInterface::available() {
  std::lock_guard<std::mutex> lock(mu_dq);
  return (receive_buffer_.empty() == false);
}
bool SocketcanInterface::support_interrupt() { return true; }
