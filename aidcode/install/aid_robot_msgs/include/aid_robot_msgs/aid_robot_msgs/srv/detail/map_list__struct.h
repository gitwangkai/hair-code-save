// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:srv/MapList.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__MAP_LIST__STRUCT_H_
#define AID_ROBOT_MSGS__SRV__DETAIL__MAP_LIST__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/MapList in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__MapList_Request
{
  uint8_t structure_needs_at_least_one_member;
} aid_robot_msgs__srv__MapList_Request;

// Struct for a sequence of aid_robot_msgs__srv__MapList_Request.
typedef struct aid_robot_msgs__srv__MapList_Request__Sequence
{
  aid_robot_msgs__srv__MapList_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__MapList_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'map_list'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MapList in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__MapList_Response
{
  bool success;
  rosidl_runtime_c__String map_list;
} aid_robot_msgs__srv__MapList_Response;

// Struct for a sequence of aid_robot_msgs__srv__MapList_Response.
typedef struct aid_robot_msgs__srv__MapList_Response__Sequence
{
  aid_robot_msgs__srv__MapList_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__MapList_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__MAP_LIST__STRUCT_H_
