// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:msg/AidPose.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_POSE__STRUCT_H_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_POSE__STRUCT_H_

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
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/AidPose in the package aid_robot_msgs.
typedef struct aid_robot_msgs__msg__AidPose
{
  std_msgs__msg__Header header;
  geometry_msgs__msg__Pose pose;
  rosidl_runtime_c__String name;
} aid_robot_msgs__msg__AidPose;

// Struct for a sequence of aid_robot_msgs__msg__AidPose.
typedef struct aid_robot_msgs__msg__AidPose__Sequence
{
  aid_robot_msgs__msg__AidPose * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__msg__AidPose__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_POSE__STRUCT_H_
