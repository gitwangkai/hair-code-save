// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from aid_robot_msgs:msg/Rectangle.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "aid_robot_msgs/msg/detail/rectangle__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace aid_robot_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void Rectangle_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aid_robot_msgs::msg::Rectangle(_init);
}

void Rectangle_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aid_robot_msgs::msg::Rectangle *>(message_memory);
  typed_message->~Rectangle();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Rectangle_message_member_array[3] = {
  {
    "center_point",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Point32>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aid_robot_msgs::msg::Rectangle, center_point),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "side_length",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aid_robot_msgs::msg::Rectangle, side_length),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "grayscale",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aid_robot_msgs::msg::Rectangle, grayscale),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Rectangle_message_members = {
  "aid_robot_msgs::msg",  // message namespace
  "Rectangle",  // message name
  3,  // number of fields
  sizeof(aid_robot_msgs::msg::Rectangle),
  Rectangle_message_member_array,  // message members
  Rectangle_init_function,  // function to initialize message memory (memory has to be allocated)
  Rectangle_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Rectangle_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Rectangle_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace aid_robot_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aid_robot_msgs::msg::Rectangle>()
{
  return &::aid_robot_msgs::msg::rosidl_typesupport_introspection_cpp::Rectangle_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aid_robot_msgs, msg, Rectangle)() {
  return &::aid_robot_msgs::msg::rosidl_typesupport_introspection_cpp::Rectangle_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
