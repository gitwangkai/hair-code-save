// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/GeneralInterface.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__GENERAL_INTERFACE__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__GENERAL_INTERFACE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/general_interface__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_GeneralInterface_Request_body
{
public:
  Init_GeneralInterface_Request_body()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::GeneralInterface_Request body(::aid_robot_msgs::srv::GeneralInterface_Request::_body_type arg)
  {
    msg_.body = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::GeneralInterface_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::GeneralInterface_Request>()
{
  return aid_robot_msgs::srv::builder::Init_GeneralInterface_Request_body();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_GeneralInterface_Response_result
{
public:
  Init_GeneralInterface_Response_result()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::GeneralInterface_Response result(::aid_robot_msgs::srv::GeneralInterface_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::GeneralInterface_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::GeneralInterface_Response>()
{
  return aid_robot_msgs::srv::builder::Init_GeneralInterface_Response_result();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__GENERAL_INTERFACE__BUILDER_HPP_
