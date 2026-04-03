// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/MapOperationAdd.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__MAP_OPERATION_ADD__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__MAP_OPERATION_ADD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/map_operation_add__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_MapOperationAdd_Request_map_file
{
public:
  explicit Init_MapOperationAdd_Request_map_file(::aid_robot_msgs::srv::MapOperationAdd_Request & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::MapOperationAdd_Request map_file(::aid_robot_msgs::srv::MapOperationAdd_Request::_map_file_type arg)
  {
    msg_.map_file = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::MapOperationAdd_Request msg_;
};

class Init_MapOperationAdd_Request_map_name
{
public:
  Init_MapOperationAdd_Request_map_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MapOperationAdd_Request_map_file map_name(::aid_robot_msgs::srv::MapOperationAdd_Request::_map_name_type arg)
  {
    msg_.map_name = std::move(arg);
    return Init_MapOperationAdd_Request_map_file(msg_);
  }

private:
  ::aid_robot_msgs::srv::MapOperationAdd_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::MapOperationAdd_Request>()
{
  return aid_robot_msgs::srv::builder::Init_MapOperationAdd_Request_map_name();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_MapOperationAdd_Response_message
{
public:
  explicit Init_MapOperationAdd_Response_message(::aid_robot_msgs::srv::MapOperationAdd_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::MapOperationAdd_Response message(::aid_robot_msgs::srv::MapOperationAdd_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::MapOperationAdd_Response msg_;
};

class Init_MapOperationAdd_Response_success
{
public:
  Init_MapOperationAdd_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MapOperationAdd_Response_message success(::aid_robot_msgs::srv::MapOperationAdd_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MapOperationAdd_Response_message(msg_);
  }

private:
  ::aid_robot_msgs::srv::MapOperationAdd_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::MapOperationAdd_Response>()
{
  return aid_robot_msgs::srv::builder::Init_MapOperationAdd_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__MAP_OPERATION_ADD__BUILDER_HPP_
