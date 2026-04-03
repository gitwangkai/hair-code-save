// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/FindBestVelocity.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/find_best_velocity__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_FindBestVelocity_Request_len
{
public:
  explicit Init_FindBestVelocity_Request_len(::aid_robot_msgs::srv::FindBestVelocity_Request & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::FindBestVelocity_Request len(::aid_robot_msgs::srv::FindBestVelocity_Request::_len_type arg)
  {
    msg_.len = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::FindBestVelocity_Request msg_;
};

class Init_FindBestVelocity_Request_max_speed
{
public:
  explicit Init_FindBestVelocity_Request_max_speed(::aid_robot_msgs::srv::FindBestVelocity_Request & msg)
  : msg_(msg)
  {}
  Init_FindBestVelocity_Request_len max_speed(::aid_robot_msgs::srv::FindBestVelocity_Request::_max_speed_type arg)
  {
    msg_.max_speed = std::move(arg);
    return Init_FindBestVelocity_Request_len(msg_);
  }

private:
  ::aid_robot_msgs::srv::FindBestVelocity_Request msg_;
};

class Init_FindBestVelocity_Request_max_angular_velocity
{
public:
  explicit Init_FindBestVelocity_Request_max_angular_velocity(::aid_robot_msgs::srv::FindBestVelocity_Request & msg)
  : msg_(msg)
  {}
  Init_FindBestVelocity_Request_max_speed max_angular_velocity(::aid_robot_msgs::srv::FindBestVelocity_Request::_max_angular_velocity_type arg)
  {
    msg_.max_angular_velocity = std::move(arg);
    return Init_FindBestVelocity_Request_max_speed(msg_);
  }

private:
  ::aid_robot_msgs::srv::FindBestVelocity_Request msg_;
};

class Init_FindBestVelocity_Request_header
{
public:
  Init_FindBestVelocity_Request_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FindBestVelocity_Request_max_angular_velocity header(::aid_robot_msgs::srv::FindBestVelocity_Request::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_FindBestVelocity_Request_max_angular_velocity(msg_);
  }

private:
  ::aid_robot_msgs::srv::FindBestVelocity_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::FindBestVelocity_Request>()
{
  return aid_robot_msgs::srv::builder::Init_FindBestVelocity_Request_header();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_FindBestVelocity_Response_msg
{
public:
  explicit Init_FindBestVelocity_Response_msg(::aid_robot_msgs::srv::FindBestVelocity_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::FindBestVelocity_Response msg(::aid_robot_msgs::srv::FindBestVelocity_Response::_msg_type arg)
  {
    msg_.msg = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::FindBestVelocity_Response msg_;
};

class Init_FindBestVelocity_Response_success
{
public:
  explicit Init_FindBestVelocity_Response_success(::aid_robot_msgs::srv::FindBestVelocity_Response & msg)
  : msg_(msg)
  {}
  Init_FindBestVelocity_Response_msg success(::aid_robot_msgs::srv::FindBestVelocity_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_FindBestVelocity_Response_msg(msg_);
  }

private:
  ::aid_robot_msgs::srv::FindBestVelocity_Response msg_;
};

class Init_FindBestVelocity_Response_cmd_vel
{
public:
  Init_FindBestVelocity_Response_cmd_vel()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FindBestVelocity_Response_success cmd_vel(::aid_robot_msgs::srv::FindBestVelocity_Response::_cmd_vel_type arg)
  {
    msg_.cmd_vel = std::move(arg);
    return Init_FindBestVelocity_Response_success(msg_);
  }

private:
  ::aid_robot_msgs::srv::FindBestVelocity_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::FindBestVelocity_Response>()
{
  return aid_robot_msgs::srv::builder::Init_FindBestVelocity_Response_cmd_vel();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__BUILDER_HPP_
