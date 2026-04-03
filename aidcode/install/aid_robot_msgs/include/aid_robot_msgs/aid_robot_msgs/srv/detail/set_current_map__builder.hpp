// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/SetCurrentMap.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__SET_CURRENT_MAP__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__SET_CURRENT_MAP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/set_current_map__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_SetCurrentMap_Request_id
{
public:
  Init_SetCurrentMap_Request_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::SetCurrentMap_Request id(::aid_robot_msgs::srv::SetCurrentMap_Request::_id_type arg)
  {
    msg_.id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::SetCurrentMap_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::SetCurrentMap_Request>()
{
  return aid_robot_msgs::srv::builder::Init_SetCurrentMap_Request_id();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_SetCurrentMap_Response_success
{
public:
  Init_SetCurrentMap_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::SetCurrentMap_Response success(::aid_robot_msgs::srv::SetCurrentMap_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::SetCurrentMap_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::SetCurrentMap_Response>()
{
  return aid_robot_msgs::srv::builder::Init_SetCurrentMap_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__SET_CURRENT_MAP__BUILDER_HPP_
