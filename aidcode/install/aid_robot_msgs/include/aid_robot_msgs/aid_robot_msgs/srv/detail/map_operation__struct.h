// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:srv/MapOperation.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__MAP_OPERATION__STRUCT_H_
#define AID_ROBOT_MSGS__SRV__DETAIL__MAP_OPERATION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'map_file_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MapOperation in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__MapOperation_Request
{
  rosidl_runtime_c__String map_file_name;
} aid_robot_msgs__srv__MapOperation_Request;

// Struct for a sequence of aid_robot_msgs__srv__MapOperation_Request.
typedef struct aid_robot_msgs__srv__MapOperation_Request__Sequence
{
  aid_robot_msgs__srv__MapOperation_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__MapOperation_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MapOperation in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__MapOperation_Response
{
  bool success;
  rosidl_runtime_c__String message;
} aid_robot_msgs__srv__MapOperation_Response;

// Struct for a sequence of aid_robot_msgs__srv__MapOperation_Response.
typedef struct aid_robot_msgs__srv__MapOperation_Response__Sequence
{
  aid_robot_msgs__srv__MapOperation_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__MapOperation_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__MAP_OPERATION__STRUCT_H_
