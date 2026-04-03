// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/ArmControl.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__ARM_CONTROL__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__ARM_CONTROL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/arm_control__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_ArmControl_Request_request
{
public:
  Init_ArmControl_Request_request()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::ArmControl_Request request(::aid_robot_msgs::srv::ArmControl_Request::_request_type arg)
  {
    msg_.request = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::ArmControl_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::ArmControl_Request>()
{
  return aid_robot_msgs::srv::builder::Init_ArmControl_Request_request();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_ArmControl_Response_response
{
public:
  Init_ArmControl_Response_response()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::ArmControl_Response response(::aid_robot_msgs::srv::ArmControl_Response::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::ArmControl_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::ArmControl_Response>()
{
  return aid_robot_msgs::srv::builder::Init_ArmControl_Response_response();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__ARM_CONTROL__BUILDER_HPP_
