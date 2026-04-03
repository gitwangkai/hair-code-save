// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/PathNav.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__PATH_NAV__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__PATH_NAV__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/path_nav__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_PathNav_Request_path
{
public:
  Init_PathNav_Request_path()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::PathNav_Request path(::aid_robot_msgs::srv::PathNav_Request::_path_type arg)
  {
    msg_.path = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::PathNav_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::PathNav_Request>()
{
  return aid_robot_msgs::srv::builder::Init_PathNav_Request_path();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_PathNav_Response_message
{
public:
  explicit Init_PathNav_Response_message(::aid_robot_msgs::srv::PathNav_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::PathNav_Response message(::aid_robot_msgs::srv::PathNav_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::PathNav_Response msg_;
};

class Init_PathNav_Response_success
{
public:
  Init_PathNav_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PathNav_Response_message success(::aid_robot_msgs::srv::PathNav_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_PathNav_Response_message(msg_);
  }

private:
  ::aid_robot_msgs::srv::PathNav_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::PathNav_Response>()
{
  return aid_robot_msgs::srv::builder::Init_PathNav_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__PATH_NAV__BUILDER_HPP_
