// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/GetDockPose.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__GET_DOCK_POSE__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__GET_DOCK_POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/get_dock_pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_GetDockPose_Request_map_id
{
public:
  Init_GetDockPose_Request_map_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::GetDockPose_Request map_id(::aid_robot_msgs::srv::GetDockPose_Request::_map_id_type arg)
  {
    msg_.map_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::GetDockPose_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::GetDockPose_Request>()
{
  return aid_robot_msgs::srv::builder::Init_GetDockPose_Request_map_id();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_GetDockPose_Response_success
{
public:
  explicit Init_GetDockPose_Response_success(::aid_robot_msgs::srv::GetDockPose_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::GetDockPose_Response success(::aid_robot_msgs::srv::GetDockPose_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::GetDockPose_Response msg_;
};

class Init_GetDockPose_Response_message
{
public:
  explicit Init_GetDockPose_Response_message(::aid_robot_msgs::srv::GetDockPose_Response & msg)
  : msg_(msg)
  {}
  Init_GetDockPose_Response_success message(::aid_robot_msgs::srv::GetDockPose_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_GetDockPose_Response_success(msg_);
  }

private:
  ::aid_robot_msgs::srv::GetDockPose_Response msg_;
};

class Init_GetDockPose_Response_point
{
public:
  Init_GetDockPose_Response_point()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetDockPose_Response_message point(::aid_robot_msgs::srv::GetDockPose_Response::_point_type arg)
  {
    msg_.point = std::move(arg);
    return Init_GetDockPose_Response_message(msg_);
  }

private:
  ::aid_robot_msgs::srv::GetDockPose_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::GetDockPose_Response>()
{
  return aid_robot_msgs::srv::builder::Init_GetDockPose_Response_point();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__GET_DOCK_POSE__BUILDER_HPP_
