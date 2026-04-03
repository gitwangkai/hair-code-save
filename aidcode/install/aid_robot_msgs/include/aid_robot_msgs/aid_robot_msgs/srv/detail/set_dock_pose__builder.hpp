// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/SetDockPose.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__SET_DOCK_POSE__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__SET_DOCK_POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/set_dock_pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_SetDockPose_Request_map_id
{
public:
  explicit Init_SetDockPose_Request_map_id(::aid_robot_msgs::srv::SetDockPose_Request & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::SetDockPose_Request map_id(::aid_robot_msgs::srv::SetDockPose_Request::_map_id_type arg)
  {
    msg_.map_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::SetDockPose_Request msg_;
};

class Init_SetDockPose_Request_point
{
public:
  Init_SetDockPose_Request_point()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetDockPose_Request_map_id point(::aid_robot_msgs::srv::SetDockPose_Request::_point_type arg)
  {
    msg_.point = std::move(arg);
    return Init_SetDockPose_Request_map_id(msg_);
  }

private:
  ::aid_robot_msgs::srv::SetDockPose_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::SetDockPose_Request>()
{
  return aid_robot_msgs::srv::builder::Init_SetDockPose_Request_point();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_SetDockPose_Response_success
{
public:
  explicit Init_SetDockPose_Response_success(::aid_robot_msgs::srv::SetDockPose_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::SetDockPose_Response success(::aid_robot_msgs::srv::SetDockPose_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::SetDockPose_Response msg_;
};

class Init_SetDockPose_Response_message
{
public:
  Init_SetDockPose_Response_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetDockPose_Response_success message(::aid_robot_msgs::srv::SetDockPose_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_SetDockPose_Response_success(msg_);
  }

private:
  ::aid_robot_msgs::srv::SetDockPose_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::SetDockPose_Response>()
{
  return aid_robot_msgs::srv::builder::Init_SetDockPose_Response_message();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__SET_DOCK_POSE__BUILDER_HPP_
