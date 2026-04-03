// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/PatrolControl.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__PATROL_CONTROL__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__PATROL_CONTROL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/patrol_control__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_PatrolControl_Request_cmd
{
public:
  Init_PatrolControl_Request_cmd()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::PatrolControl_Request cmd(::aid_robot_msgs::srv::PatrolControl_Request::_cmd_type arg)
  {
    msg_.cmd = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::PatrolControl_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::PatrolControl_Request>()
{
  return aid_robot_msgs::srv::builder::Init_PatrolControl_Request_cmd();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_PatrolControl_Response_message
{
public:
  explicit Init_PatrolControl_Response_message(::aid_robot_msgs::srv::PatrolControl_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::PatrolControl_Response message(::aid_robot_msgs::srv::PatrolControl_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::PatrolControl_Response msg_;
};

class Init_PatrolControl_Response_success
{
public:
  Init_PatrolControl_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PatrolControl_Response_message success(::aid_robot_msgs::srv::PatrolControl_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_PatrolControl_Response_message(msg_);
  }

private:
  ::aid_robot_msgs::srv::PatrolControl_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::PatrolControl_Response>()
{
  return aid_robot_msgs::srv::builder::Init_PatrolControl_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__PATROL_CONTROL__BUILDER_HPP_
