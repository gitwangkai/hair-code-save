// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:srv/GetString.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__GET_STRING__STRUCT_H_
#define AID_ROBOT_MSGS__SRV__DETAIL__GET_STRING__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetString in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__GetString_Request
{
  uint8_t structure_needs_at_least_one_member;
} aid_robot_msgs__srv__GetString_Request;

// Struct for a sequence of aid_robot_msgs__srv__GetString_Request.
typedef struct aid_robot_msgs__srv__GetString_Request__Sequence
{
  aid_robot_msgs__srv__GetString_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__GetString_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// Member 'result'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetString in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__GetString_Response
{
  bool success;
  rosidl_runtime_c__String message;
  rosidl_runtime_c__String result;
} aid_robot_msgs__srv__GetString_Response;

// Struct for a sequence of aid_robot_msgs__srv__GetString_Response.
typedef struct aid_robot_msgs__srv__GetString_Response__Sequence
{
  aid_robot_msgs__srv__GetString_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__GetString_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__GET_STRING__STRUCT_H_
