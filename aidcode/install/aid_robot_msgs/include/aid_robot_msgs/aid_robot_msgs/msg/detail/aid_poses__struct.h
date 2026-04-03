// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:msg/AidPoses.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_POSES__STRUCT_H_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_POSES__STRUCT_H_

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
// Member 'poses'
#include "aid_robot_msgs/msg/detail/aid_pose__struct.h"

/// Struct defined in msg/AidPoses in the package aid_robot_msgs.
typedef struct aid_robot_msgs__msg__AidPoses
{
  std_msgs__msg__Header header;
  aid_robot_msgs__msg__AidPose__Sequence poses;
} aid_robot_msgs__msg__AidPoses;

// Struct for a sequence of aid_robot_msgs__msg__AidPoses.
typedef struct aid_robot_msgs__msg__AidPoses__Sequence
{
  aid_robot_msgs__msg__AidPoses * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__msg__AidPoses__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_POSES__STRUCT_H_
