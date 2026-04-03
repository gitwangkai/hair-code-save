// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/GetCurrentMap.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_MAP__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_MAP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/get_current_map__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::GetCurrentMap_Request>()
{
  return ::aid_robot_msgs::srv::GetCurrentMap_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_GetCurrentMap_Response_map_name
{
public:
  explicit Init_GetCurrentMap_Response_map_name(::aid_robot_msgs::srv::GetCurrentMap_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::GetCurrentMap_Response map_name(::aid_robot_msgs::srv::GetCurrentMap_Response::_map_name_type arg)
  {
    msg_.map_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::GetCurrentMap_Response msg_;
};

class Init_GetCurrentMap_Response_map_file
{
public:
  explicit Init_GetCurrentMap_Response_map_file(::aid_robot_msgs::srv::GetCurrentMap_Response & msg)
  : msg_(msg)
  {}
  Init_GetCurrentMap_Response_map_name map_file(::aid_robot_msgs::srv::GetCurrentMap_Response::_map_file_type arg)
  {
    msg_.map_file = std::move(arg);
    return Init_GetCurrentMap_Response_map_name(msg_);
  }

private:
  ::aid_robot_msgs::srv::GetCurrentMap_Response msg_;
};

class Init_GetCurrentMap_Response_map_id
{
public:
  explicit Init_GetCurrentMap_Response_map_id(::aid_robot_msgs::srv::GetCurrentMap_Response & msg)
  : msg_(msg)
  {}
  Init_GetCurrentMap_Response_map_file map_id(::aid_robot_msgs::srv::GetCurrentMap_Response::_map_id_type arg)
  {
    msg_.map_id = std::move(arg);
    return Init_GetCurrentMap_Response_map_file(msg_);
  }

private:
  ::aid_robot_msgs::srv::GetCurrentMap_Response msg_;
};

class Init_GetCurrentMap_Response_success
{
public:
  Init_GetCurrentMap_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetCurrentMap_Response_map_id success(::aid_robot_msgs::srv::GetCurrentMap_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GetCurrentMap_Response_map_id(msg_);
  }

private:
  ::aid_robot_msgs::srv::GetCurrentMap_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::GetCurrentMap_Response>()
{
  return aid_robot_msgs::srv::builder::Init_GetCurrentMap_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_MAP__BUILDER_HPP_
