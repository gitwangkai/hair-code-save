// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:srv/SetCurrentMap.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__SET_CURRENT_MAP__STRUCT_H_
#define AID_ROBOT_MSGS__SRV__DETAIL__SET_CURRENT_MAP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/SetCurrentMap in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__SetCurrentMap_Request
{
  uint32_t id;
} aid_robot_msgs__srv__SetCurrentMap_Request;

// Struct for a sequence of aid_robot_msgs__srv__SetCurrentMap_Request.
typedef struct aid_robot_msgs__srv__SetCurrentMap_Request__Sequence
{
  aid_robot_msgs__srv__SetCurrentMap_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__SetCurrentMap_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/SetCurrentMap in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__SetCurrentMap_Response
{
  bool success;
} aid_robot_msgs__srv__SetCurrentMap_Response;

// Struct for a sequence of aid_robot_msgs__srv__SetCurrentMap_Response.
typedef struct aid_robot_msgs__srv__SetCurrentMap_Response__Sequence
{
  aid_robot_msgs__srv__SetCurrentMap_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__SetCurrentMap_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__SET_CURRENT_MAP__STRUCT_H_
