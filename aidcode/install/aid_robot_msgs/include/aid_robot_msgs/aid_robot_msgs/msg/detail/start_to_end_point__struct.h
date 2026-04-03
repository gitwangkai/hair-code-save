// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:msg/StartToEndPoint.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__STRUCT_H_
#define AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'start'
// Member 'end'
#include "geometry_msgs/msg/detail/point32__struct.h"

/// Struct defined in msg/StartToEndPoint in the package aid_robot_msgs.
typedef struct aid_robot_msgs__msg__StartToEndPoint
{
  geometry_msgs__msg__Point32 start;
  geometry_msgs__msg__Point32 end;
} aid_robot_msgs__msg__StartToEndPoint;

// Struct for a sequence of aid_robot_msgs__msg__StartToEndPoint.
typedef struct aid_robot_msgs__msg__StartToEndPoint__Sequence
{
  aid_robot_msgs__msg__StartToEndPoint * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__msg__StartToEndPoint__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__STRUCT_H_
