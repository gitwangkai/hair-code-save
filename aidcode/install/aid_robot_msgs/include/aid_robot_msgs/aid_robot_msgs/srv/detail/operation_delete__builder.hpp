// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/OperationDelete.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__OPERATION_DELETE__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__OPERATION_DELETE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/operation_delete__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_OperationDelete_Request_data_type
{
public:
  explicit Init_OperationDelete_Request_data_type(::aid_robot_msgs::srv::OperationDelete_Request & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::OperationDelete_Request data_type(::aid_robot_msgs::srv::OperationDelete_Request::_data_type_type arg)
  {
    msg_.data_type = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::OperationDelete_Request msg_;
};

class Init_OperationDelete_Request_id
{
public:
  Init_OperationDelete_Request_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_OperationDelete_Request_data_type id(::aid_robot_msgs::srv::OperationDelete_Request::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_OperationDelete_Request_data_type(msg_);
  }

private:
  ::aid_robot_msgs::srv::OperationDelete_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::OperationDelete_Request>()
{
  return aid_robot_msgs::srv::builder::Init_OperationDelete_Request_id();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_OperationDelete_Response_message
{
public:
  explicit Init_OperationDelete_Response_message(::aid_robot_msgs::srv::OperationDelete_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::OperationDelete_Response message(::aid_robot_msgs::srv::OperationDelete_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::OperationDelete_Response msg_;
};

class Init_OperationDelete_Response_success
{
public:
  Init_OperationDelete_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_OperationDelete_Response_message success(::aid_robot_msgs::srv::OperationDelete_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_OperationDelete_Response_message(msg_);
  }

private:
  ::aid_robot_msgs::srv::OperationDelete_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::OperationDelete_Response>()
{
  return aid_robot_msgs::srv::builder::Init_OperationDelete_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__OPERATION_DELETE__BUILDER_HPP_
