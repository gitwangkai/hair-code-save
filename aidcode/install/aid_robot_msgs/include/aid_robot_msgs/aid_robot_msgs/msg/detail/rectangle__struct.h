// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:msg/Rectangle.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__RECTANGLE__STRUCT_H_
#define AID_ROBOT_MSGS__MSG__DETAIL__RECTANGLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'center_point'
#include "geometry_msgs/msg/detail/point32__struct.h"

/// Struct defined in msg/Rectangle in the package aid_robot_msgs.
typedef struct aid_robot_msgs__msg__Rectangle
{
  geometry_msgs__msg__Point32 center_point;
  float side_length;
  uint8_t grayscale;
} aid_robot_msgs__msg__Rectangle;

// Struct for a sequence of aid_robot_msgs__msg__Rectangle.
typedef struct aid_robot_msgs__msg__Rectangle__Sequence
{
  aid_robot_msgs__msg__Rectangle * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__msg__Rectangle__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__RECTANGLE__STRUCT_H_
