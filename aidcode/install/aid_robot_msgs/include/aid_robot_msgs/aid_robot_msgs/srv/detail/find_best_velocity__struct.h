// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:srv/FindBestVelocity.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__STRUCT_H_
#define AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in srv/FindBestVelocity in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__FindBestVelocity_Request
{
  std_msgs__msg__Header header;
  float max_angular_velocity;
  float max_speed;
  float len;
} aid_robot_msgs__srv__FindBestVelocity_Request;

// Struct for a sequence of aid_robot_msgs__srv__FindBestVelocity_Request.
typedef struct aid_robot_msgs__srv__FindBestVelocity_Request__Sequence
{
  aid_robot_msgs__srv__FindBestVelocity_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__FindBestVelocity_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'cmd_vel'
#include "geometry_msgs/msg/detail/twist__struct.h"
// Member 'msg'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/FindBestVelocity in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__FindBestVelocity_Response
{
  geometry_msgs__msg__Twist cmd_vel;
  bool success;
  rosidl_runtime_c__String msg;
} aid_robot_msgs__srv__FindBestVelocity_Response;

// Struct for a sequence of aid_robot_msgs__srv__FindBestVelocity_Response.
typedef struct aid_robot_msgs__srv__FindBestVelocity_Response__Sequence
{
  aid_robot_msgs__srv__FindBestVelocity_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__FindBestVelocity_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__STRUCT_H_
