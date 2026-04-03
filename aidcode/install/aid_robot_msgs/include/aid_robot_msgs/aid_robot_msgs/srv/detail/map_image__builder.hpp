// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/MapImage.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__MAP_IMAGE__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__MAP_IMAGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/map_image__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_MapImage_Request_id
{
public:
  Init_MapImage_Request_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aid_robot_msgs::srv::MapImage_Request id(::aid_robot_msgs::srv::MapImage_Request::_id_type arg)
  {
    msg_.id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::MapImage_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::MapImage_Request>()
{
  return aid_robot_msgs::srv::builder::Init_MapImage_Request_id();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_MapImage_Response_map_file
{
public:
  explicit Init_MapImage_Response_map_file(::aid_robot_msgs::srv::MapImage_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::MapImage_Response map_file(::aid_robot_msgs::srv::MapImage_Response::_map_file_type arg)
  {
    msg_.map_file = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::MapImage_Response msg_;
};

class Init_MapImage_Response_map
{
public:
  explicit Init_MapImage_Response_map(::aid_robot_msgs::srv::MapImage_Response & msg)
  : msg_(msg)
  {}
  Init_MapImage_Response_map_file map(::aid_robot_msgs::srv::MapImage_Response::_map_type arg)
  {
    msg_.map = std::move(arg);
    return Init_MapImage_Response_map_file(msg_);
  }

private:
  ::aid_robot_msgs::srv::MapImage_Response msg_;
};

class Init_MapImage_Response_success
{
public:
  Init_MapImage_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MapImage_Response_map success(::aid_robot_msgs::srv::MapImage_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MapImage_Response_map(msg_);
  }

private:
  ::aid_robot_msgs::srv::MapImage_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::MapImage_Response>()
{
  return aid_robot_msgs::srv::builder::Init_MapImage_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__MAP_IMAGE__BUILDER_HPP_
