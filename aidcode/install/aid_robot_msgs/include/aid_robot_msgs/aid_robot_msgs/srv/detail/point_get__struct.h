// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:srv/PointGet.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__POINT_GET__STRUCT_H_
#define AID_ROBOT_MSGS__SRV__DETAIL__POINT_GET__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'data_type'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/PointGet in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__PointGet_Request
{
  uint32_t id;
  rosidl_runtime_c__String data_type;
} aid_robot_msgs__srv__PointGet_Request;

// Struct for a sequence of aid_robot_msgs__srv__PointGet_Request.
typedef struct aid_robot_msgs__srv__PointGet_Request__Sequence
{
  aid_robot_msgs__srv__PointGet_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__PointGet_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "aid_robot_msgs/msg/detail/aid_pose__struct.h"

/// Struct defined in srv/PointGet in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__PointGet_Response
{
  bool success;
  aid_robot_msgs__msg__AidPose message;
} aid_robot_msgs__srv__PointGet_Response;

// Struct for a sequence of aid_robot_msgs__srv__PointGet_Response.
typedef struct aid_robot_msgs__srv__PointGet_Response__Sequence
{
  aid_robot_msgs__srv__PointGet_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__PointGet_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__POINT_GET__STRUCT_H_
