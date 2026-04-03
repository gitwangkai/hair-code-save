// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:msg/StartToEndPoint.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__BUILDER_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/msg/detail/start_to_end_point__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace msg
{

namespace builder
{

class Init_StartToEndPoint_end
{
public:
  explicit Init_StartToEndPoint_end(::aid_robot_msgs::msg::StartToEndPoint & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::msg::StartToEndPoint end(::aid_robot_msgs::msg::StartToEndPoint::_end_type arg)
  {
    msg_.end = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::msg::StartToEndPoint msg_;
};

class Init_StartToEndPoint_start
{
public:
  Init_StartToEndPoint_start()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_StartToEndPoint_end start(::aid_robot_msgs::msg::StartToEndPoint::_start_type arg)
  {
    msg_.start = std::move(arg);
    return Init_StartToEndPoint_end(msg_);
  }

private:
  ::aid_robot_msgs::msg::StartToEndPoint msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::msg::StartToEndPoint>()
{
  return aid_robot_msgs::msg::builder::Init_StartToEndPoint_start();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__BUILDER_HPP_
