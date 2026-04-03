// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:msg/Rectangle.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__RECTANGLE__BUILDER_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__RECTANGLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/msg/detail/rectangle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace msg
{

namespace builder
{

class Init_Rectangle_grayscale
{
public:
  explicit Init_Rectangle_grayscale(::aid_robot_msgs::msg::Rectangle & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::msg::Rectangle grayscale(::aid_robot_msgs::msg::Rectangle::_grayscale_type arg)
  {
    msg_.grayscale = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::msg::Rectangle msg_;
};

class Init_Rectangle_side_length
{
public:
  explicit Init_Rectangle_side_length(::aid_robot_msgs::msg::Rectangle & msg)
  : msg_(msg)
  {}
  Init_Rectangle_grayscale side_length(::aid_robot_msgs::msg::Rectangle::_side_length_type arg)
  {
    msg_.side_length = std::move(arg);
    return Init_Rectangle_grayscale(msg_);
  }

private:
  ::aid_robot_msgs::msg::Rectangle msg_;
};

class Init_Rectangle_center_point
{
public:
  Init_Rectangle_center_point()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Rectangle_side_length center_point(::aid_robot_msgs::msg::Rectangle::_center_point_type arg)
  {
    msg_.center_point = std::move(arg);
    return Init_Rectangle_side_length(msg_);
  }

private:
  ::aid_robot_msgs::msg::Rectangle msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::msg::Rectangle>()
{
  return aid_robot_msgs::msg::builder::Init_Rectangle_center_point();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__RECTANGLE__BUILDER_HPP_
