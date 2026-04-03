// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/ForbiddenGet.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__FORBIDDEN_GET__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__FORBIDDEN_GET__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/forbidden_get__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_ForbiddenGet_Request_map_id
{
public:
  Init_ForbiddenGet_Request_map_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::ForbiddenGet_Request map_id(::aid_robot_msgs::srv::ForbiddenGet_Request::_map_id_type arg)
  {
    msg_.map_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::ForbiddenGet_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::ForbiddenGet_Request>()
{
  return aid_robot_msgs::srv::builder::Init_ForbiddenGet_Request_map_id();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_ForbiddenGet_Response_lines
{
public:
  explicit Init_ForbiddenGet_Response_lines(::aid_robot_msgs::srv::ForbiddenGet_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::ForbiddenGet_Response lines(::aid_robot_msgs::srv::ForbiddenGet_Response::_lines_type arg)
  {
    msg_.lines = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::ForbiddenGet_Response msg_;
};

class Init_ForbiddenGet_Response_message
{
public:
  explicit Init_ForbiddenGet_Response_message(::aid_robot_msgs::srv::ForbiddenGet_Response & msg)
  : msg_(msg)
  {}
  Init_ForbiddenGet_Response_lines message(::aid_robot_msgs::srv::ForbiddenGet_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_ForbiddenGet_Response_lines(msg_);
  }

private:
  ::aid_robot_msgs::srv::ForbiddenGet_Response msg_;
};

class Init_ForbiddenGet_Response_success
{
public:
  Init_ForbiddenGet_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ForbiddenGet_Response_message success(::aid_robot_msgs::srv::ForbiddenGet_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ForbiddenGet_Response_message(msg_);
  }

private:
  ::aid_robot_msgs::srv::ForbiddenGet_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::ForbiddenGet_Response>()
{
  return aid_robot_msgs::srv::builder::Init_ForbiddenGet_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__FORBIDDEN_GET__BUILDER_HPP_
