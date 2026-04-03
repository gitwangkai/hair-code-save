// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:msg/FilterCloud.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__FILTER_CLOUD__BUILDER_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__FILTER_CLOUD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/msg/detail/filter_cloud__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace msg
{

namespace builder
{

class Init_FilterCloud_raw_points
{
public:
  explicit Init_FilterCloud_raw_points(::aid_robot_msgs::msg::FilterCloud & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::msg::FilterCloud raw_points(::aid_robot_msgs::msg::FilterCloud::_raw_points_type arg)
  {
    msg_.raw_points = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::msg::FilterCloud msg_;
};

class Init_FilterCloud_filtered_points
{
public:
  explicit Init_FilterCloud_filtered_points(::aid_robot_msgs::msg::FilterCloud & msg)
  : msg_(msg)
  {}
  Init_FilterCloud_raw_points filtered_points(::aid_robot_msgs::msg::FilterCloud::_filtered_points_type arg)
  {
    msg_.filtered_points = std::move(arg);
    return Init_FilterCloud_raw_points(msg_);
  }

private:
  ::aid_robot_msgs::msg::FilterCloud msg_;
};

class Init_FilterCloud_header
{
public:
  Init_FilterCloud_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FilterCloud_filtered_points header(::aid_robot_msgs::msg::FilterCloud::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_FilterCloud_filtered_points(msg_);
  }

private:
  ::aid_robot_msgs::msg::FilterCloud msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::msg::FilterCloud>()
{
  return aid_robot_msgs::msg::builder::Init_FilterCloud_header();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__FILTER_CLOUD__BUILDER_HPP_
