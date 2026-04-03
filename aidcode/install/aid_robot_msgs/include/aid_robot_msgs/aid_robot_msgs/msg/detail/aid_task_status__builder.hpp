// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:msg/AidTaskStatus.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__BUILDER_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/msg/detail/aid_task_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace msg
{

namespace builder
{

class Init_AidTaskStatus_task_type
{
public:
  explicit Init_AidTaskStatus_task_type(::aid_robot_msgs::msg::AidTaskStatus & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::msg::AidTaskStatus task_type(::aid_robot_msgs::msg::AidTaskStatus::_task_type_type arg)
  {
    msg_.task_type = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::msg::AidTaskStatus msg_;
};

class Init_AidTaskStatus_status
{
public:
  Init_AidTaskStatus_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AidTaskStatus_task_type status(::aid_robot_msgs::msg::AidTaskStatus::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_AidTaskStatus_task_type(msg_);
  }

private:
  ::aid_robot_msgs::msg::AidTaskStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::msg::AidTaskStatus>()
{
  return aid_robot_msgs::msg::builder::Init_AidTaskStatus_status();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__BUILDER_HPP_
