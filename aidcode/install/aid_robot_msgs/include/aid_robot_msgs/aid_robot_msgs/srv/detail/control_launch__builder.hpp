// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/ControlLaunch.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__CONTROL_LAUNCH__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__CONTROL_LAUNCH__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/control_launch__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_ControlLaunch_Request_parameter
{
public:
  explicit Init_ControlLaunch_Request_parameter(::aid_robot_msgs::srv::ControlLaunch_Request & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::ControlLaunch_Request parameter(::aid_robot_msgs::srv::ControlLaunch_Request::_parameter_type arg)
  {
    msg_.parameter = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::ControlLaunch_Request msg_;
};

class Init_ControlLaunch_Request_launch_file
{
public:
  Init_ControlLaunch_Request_launch_file()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ControlLaunch_Request_parameter launch_file(::aid_robot_msgs::srv::ControlLaunch_Request::_launch_file_type arg)
  {
    msg_.launch_file = std::move(arg);
    return Init_ControlLaunch_Request_parameter(msg_);
  }

private:
  ::aid_robot_msgs::srv::ControlLaunch_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::ControlLaunch_Request>()
{
  return aid_robot_msgs::srv::builder::Init_ControlLaunch_Request_launch_file();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_ControlLaunch_Response_message
{
public:
  explicit Init_ControlLaunch_Response_message(::aid_robot_msgs::srv::ControlLaunch_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::ControlLaunch_Response message(::aid_robot_msgs::srv::ControlLaunch_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::ControlLaunch_Response msg_;
};

class Init_ControlLaunch_Response_success
{
public:
  Init_ControlLaunch_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ControlLaunch_Response_message success(::aid_robot_msgs::srv::ControlLaunch_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ControlLaunch_Response_message(msg_);
  }

private:
  ::aid_robot_msgs::srv::ControlLaunch_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::ControlLaunch_Response>()
{
  return aid_robot_msgs::srv::builder::Init_ControlLaunch_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__CONTROL_LAUNCH__BUILDER_HPP_
