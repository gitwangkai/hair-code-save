// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from aid_robot_msgs:msg/AidTaskStatus.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "aid_robot_msgs/msg/detail/aid_task_status__struct.hpp"
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

void AidTaskStatus_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aid_robot_msgs::msg::AidTaskStatus(_init);
}

void AidTaskStatus_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aid_robot_msgs::msg::AidTaskStatus *>(message_memory);
  typed_message->~AidTaskStatus();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember AidTaskStatus_message_member_array[2] = {
  {
    "status",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aid_robot_msgs::msg::AidTaskStatus, status),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "task_type",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aid_robot_msgs::msg::AidTaskStatus, task_type),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers AidTaskStatus_message_members = {
  "aid_robot_msgs::msg",  // message namespace
  "AidTaskStatus",  // message name
  2,  // number of fields
  sizeof(aid_robot_msgs::msg::AidTaskStatus),
  AidTaskStatus_message_member_array,  // message members
  AidTaskStatus_init_function,  // function to initialize message memory (memory has to be allocated)
  AidTaskStatus_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t AidTaskStatus_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &AidTaskStatus_message_members,
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
get_message_type_support_handle<aid_robot_msgs::msg::AidTaskStatus>()
{
  return &::aid_robot_msgs::msg::rosidl_typesupport_introspection_cpp::AidTaskStatus_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aid_robot_msgs, msg, AidTaskStatus)() {
  return &::aid_robot_msgs::msg::rosidl_typesupport_introspection_cpp::AidTaskStatus_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
