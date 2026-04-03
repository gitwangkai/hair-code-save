// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:srv/ArmControl.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__ARM_CONTROL__STRUCT_H_
#define AID_ROBOT_MSGS__SRV__DETAIL__ARM_CONTROL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'request'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ArmControl in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__ArmControl_Request
{
  rosidl_runtime_c__String request;
} aid_robot_msgs__srv__ArmControl_Request;

// Struct for a sequence of aid_robot_msgs__srv__ArmControl_Request.
typedef struct aid_robot_msgs__srv__ArmControl_Request__Sequence
{
  aid_robot_msgs__srv__ArmControl_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__ArmControl_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'response'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ArmControl in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__ArmControl_Response
{
  rosidl_runtime_c__String response;
} aid_robot_msgs__srv__ArmControl_Response;

// Struct for a sequence of aid_robot_msgs__srv__ArmControl_Response.
typedef struct aid_robot_msgs__srv__ArmControl_Response__Sequence
{
  aid_robot_msgs__srv__ArmControl_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__ArmControl_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__ARM_CONTROL__STRUCT_H_
