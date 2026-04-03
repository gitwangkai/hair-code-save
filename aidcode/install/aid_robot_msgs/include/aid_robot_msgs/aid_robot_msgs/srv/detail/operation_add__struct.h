// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:srv/OperationAdd.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__OPERATION_ADD__STRUCT_H_
#define AID_ROBOT_MSGS__SRV__DETAIL__OPERATION_ADD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'frame_id'
// Member 'data'
// Member 'data_type'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/OperationAdd in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__OperationAdd_Request
{
  uint32_t map_id;
  rosidl_runtime_c__String frame_id;
  rosidl_runtime_c__String data;
  rosidl_runtime_c__String data_type;
} aid_robot_msgs__srv__OperationAdd_Request;

// Struct for a sequence of aid_robot_msgs__srv__OperationAdd_Request.
typedef struct aid_robot_msgs__srv__OperationAdd_Request__Sequence
{
  aid_robot_msgs__srv__OperationAdd_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__OperationAdd_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/OperationAdd in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__OperationAdd_Response
{
  bool success;
  rosidl_runtime_c__String message;
} aid_robot_msgs__srv__OperationAdd_Response;

// Struct for a sequence of aid_robot_msgs__srv__OperationAdd_Response.
typedef struct aid_robot_msgs__srv__OperationAdd_Response__Sequence
{
  aid_robot_msgs__srv__OperationAdd_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__OperationAdd_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__OPERATION_ADD__STRUCT_H_
