// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:msg/BoolSensor.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__BOOL_SENSOR__BUILDER_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__BOOL_SENSOR__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/msg/detail/bool_sensor__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace msg
{

namespace builder
{

class Init_BoolSensor_triggered
{
public:
  explicit Init_BoolSensor_triggered(::aid_robot_msgs::msg::BoolSensor & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::msg::BoolSensor triggered(::aid_robot_msgs::msg::BoolSensor::_triggered_type arg)
  {
    msg_.triggered = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::msg::BoolSensor msg_;
};

class Init_BoolSensor_header
{
public:
  Init_BoolSensor_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_BoolSensor_triggered header(::aid_robot_msgs::msg::BoolSensor::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_BoolSensor_triggered(msg_);
  }

private:
  ::aid_robot_msgs::msg::BoolSensor msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::msg::BoolSensor>()
{
  return aid_robot_msgs::msg::builder::Init_BoolSensor_header();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__BOOL_SENSOR__BUILDER_HPP_
