// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/StatusChange.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__STATUS_CHANGE__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__STATUS_CHANGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/status_change__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_StatusChange_Request_action
{
public:
  Init_StatusChange_Request_action()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::StatusChange_Request action(::aid_robot_msgs::srv::StatusChange_Request::_action_type arg)
  {
    msg_.action = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::StatusChange_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::StatusChange_Request>()
{
  return aid_robot_msgs::srv::builder::Init_StatusChange_Request_action();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_StatusChange_Response_message
{
public:
  Init_StatusChange_Response_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::StatusChange_Response message(::aid_robot_msgs::srv::StatusChange_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::StatusChange_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::StatusChange_Response>()
{
  return aid_robot_msgs::srv::builder::Init_StatusChange_Response_message();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__STATUS_CHANGE__BUILDER_HPP_
