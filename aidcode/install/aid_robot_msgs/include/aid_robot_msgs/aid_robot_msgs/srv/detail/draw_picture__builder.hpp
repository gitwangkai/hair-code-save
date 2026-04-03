// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aid_robot_msgs:srv/DrawPicture.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__DRAW_PICTURE__BUILDER_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__DRAW_PICTURE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aid_robot_msgs/srv/detail/draw_picture__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_DrawPicture_Request_rectangle_array
{
public:
  explicit Init_DrawPicture_Request_rectangle_array(::aid_robot_msgs::srv::DrawPicture_Request & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::DrawPicture_Request rectangle_array(::aid_robot_msgs::srv::DrawPicture_Request::_rectangle_array_type arg)
  {
    msg_.rectangle_array = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::DrawPicture_Request msg_;
};

class Init_DrawPicture_Request_data
{
public:
  explicit Init_DrawPicture_Request_data(::aid_robot_msgs::srv::DrawPicture_Request & msg)
  : msg_(msg)
  {}
  Init_DrawPicture_Request_rectangle_array data(::aid_robot_msgs::srv::DrawPicture_Request::_data_type arg)
  {
    msg_.data = std::move(arg);
    return Init_DrawPicture_Request_rectangle_array(msg_);
  }

private:
  ::aid_robot_msgs::srv::DrawPicture_Request msg_;
};

class Init_DrawPicture_Request_map_id
{
public:
  explicit Init_DrawPicture_Request_map_id(::aid_robot_msgs::srv::DrawPicture_Request & msg)
  : msg_(msg)
  {}
  Init_DrawPicture_Request_data map_id(::aid_robot_msgs::srv::DrawPicture_Request::_map_id_type arg)
  {
    msg_.map_id = std::move(arg);
    return Init_DrawPicture_Request_data(msg_);
  }

private:
  ::aid_robot_msgs::srv::DrawPicture_Request msg_;
};

class Init_DrawPicture_Request_type
{
public:
  explicit Init_DrawPicture_Request_type(::aid_robot_msgs::srv::DrawPicture_Request & msg)
  : msg_(msg)
  {}
  Init_DrawPicture_Request_map_id type(::aid_robot_msgs::srv::DrawPicture_Request::_type_type arg)
  {
    msg_.type = std::move(arg);
    return Init_DrawPicture_Request_map_id(msg_);
  }

private:
  ::aid_robot_msgs::srv::DrawPicture_Request msg_;
};

class Init_DrawPicture_Request_frame_id
{
public:
  Init_DrawPicture_Request_frame_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DrawPicture_Request_type frame_id(::aid_robot_msgs::srv::DrawPicture_Request::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return Init_DrawPicture_Request_type(msg_);
  }

private:
  ::aid_robot_msgs::srv::DrawPicture_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::DrawPicture_Request>()
{
  return aid_robot_msgs::srv::builder::Init_DrawPicture_Request_frame_id();
}

}  // namespace aid_robot_msgs


namespace aid_robot_msgs
{

namespace srv
{

namespace builder
{

class Init_DrawPicture_Response_message
{
public:
  explicit Init_DrawPicture_Response_message(::aid_robot_msgs::srv::DrawPicture_Response & msg)
  : msg_(msg)
  {}
  ::aid_robot_msgs::srv::DrawPicture_Response message(::aid_robot_msgs::srv::DrawPicture_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aid_robot_msgs::srv::DrawPicture_Response msg_;
};

class Init_DrawPicture_Response_success
{
public:
  Init_DrawPicture_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DrawPicture_Response_message success(::aid_robot_msgs::srv::DrawPicture_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_DrawPicture_Response_message(msg_);
  }

private:
  ::aid_robot_msgs::srv::DrawPicture_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aid_robot_msgs::srv::DrawPicture_Response>()
{
  return aid_robot_msgs::srv::builder::Init_DrawPicture_Response_success();
}

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__DRAW_PICTURE__BUILDER_HPP_
