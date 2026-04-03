// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:msg/AidPoses.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_POSES__BUILDER_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_POSES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/msg/detail/aid_poses__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace msg
{

namespace builder
{

class Init_AidPoses_poses
{
public:
  explicit Init_AidPoses_poses(::aid_robot_msgs::msg::AidPoses & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::msg::AidPoses poses(::aid_robot_msgs::msg::AidPoses::_poses_type arg)
  {
    msg_.poses = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::msg::AidPoses msg_;
};

class Init_AidPoses_header
{
public:
  Init_AidPoses_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AidPoses_poses header(::aid_robot_msgs::msg::AidPoses::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_AidPoses_poses(msg_);
  }

private:
  ::aid_robot_msgs::msg::AidPoses msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::msg::AidPoses>()
{
  return aid_robot_msgs::msg::builder::Init_AidPoses_header();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_POSES__BUILDER_HPP_
