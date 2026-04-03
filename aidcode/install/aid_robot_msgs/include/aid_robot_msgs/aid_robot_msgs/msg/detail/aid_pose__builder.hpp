// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:msg/AidPose.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_POSE__BUILDER_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/msg/detail/aid_pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace msg
{

namespace builder
{

class Init_AidPose_name
{
public:
  explicit Init_AidPose_name(::aid_robot_msgs::msg::AidPose & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::msg::AidPose name(::aid_robot_msgs::msg::AidPose::_name_type arg)
  {
    msg_.name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::msg::AidPose msg_;
};

class Init_AidPose_pose
{
public:
  explicit Init_AidPose_pose(::aid_robot_msgs::msg::AidPose & msg)
  : msg_(msg)
  {}
  Init_AidPose_name pose(::aid_robot_msgs::msg::AidPose::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_AidPose_name(msg_);
  }

private:
  ::aid_robot_msgs::msg::AidPose msg_;
};

class Init_AidPose_header
{
public:
  Init_AidPose_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AidPose_pose header(::aid_robot_msgs::msg::AidPose::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_AidPose_pose(msg_);
  }

private:
  ::aid_robot_msgs::msg::AidPose msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::msg::AidPose>()
{
  return aid_robot_msgs::msg::builder::Init_AidPose_header();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_POSE__BUILDER_HPP_
