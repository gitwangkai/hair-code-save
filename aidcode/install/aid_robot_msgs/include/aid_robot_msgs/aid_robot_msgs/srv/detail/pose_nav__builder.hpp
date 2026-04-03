// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/PoseNav.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__POSE_NAV__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__POSE_NAV__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/pose_nav__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_PoseNav_Request_pose
{
public:
  Init_PoseNav_Request_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::PoseNav_Request pose(::aid_robot_msgs::srv::PoseNav_Request::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::PoseNav_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::PoseNav_Request>()
{
  return aid_robot_msgs::srv::builder::Init_PoseNav_Request_pose();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_PoseNav_Response_message
{
public:
  explicit Init_PoseNav_Response_message(::aid_robot_msgs::srv::PoseNav_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::PoseNav_Response message(::aid_robot_msgs::srv::PoseNav_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::PoseNav_Response msg_;
};

class Init_PoseNav_Response_success
{
public:
  Init_PoseNav_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PoseNav_Response_message success(::aid_robot_msgs::srv::PoseNav_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_PoseNav_Response_message(msg_);
  }

private:
  ::aid_robot_msgs::srv::PoseNav_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::PoseNav_Response>()
{
  return aid_robot_msgs::srv::builder::Init_PoseNav_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__POSE_NAV__BUILDER_HPP_
