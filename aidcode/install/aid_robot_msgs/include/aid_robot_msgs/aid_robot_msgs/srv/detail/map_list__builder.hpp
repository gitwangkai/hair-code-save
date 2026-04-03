// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/MapList.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__MAP_LIST__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__MAP_LIST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/map_list__struct.hpp"
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
auto build<::aid_robot_msgs::srv::MapList_Request>()
{
  return ::aid_robot_msgs::srv::MapList_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_MapList_Response_map_list
{
public:
  explicit Init_MapList_Response_map_list(::aid_robot_msgs::srv::MapList_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::MapList_Response map_list(::aid_robot_msgs::srv::MapList_Response::_map_list_type arg)
  {
    msg_.map_list = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::MapList_Response msg_;
};

class Init_MapList_Response_success
{
public:
  Init_MapList_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MapList_Response_map_list success(::aid_robot_msgs::srv::MapList_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MapList_Response_map_list(msg_);
  }

private:
  ::aid_robot_msgs::srv::MapList_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::MapList_Response>()
{
  return aid_robot_msgs::srv::builder::Init_MapList_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__MAP_LIST__BUILDER_HPP_
