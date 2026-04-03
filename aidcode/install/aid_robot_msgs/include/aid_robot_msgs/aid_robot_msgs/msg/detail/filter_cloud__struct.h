// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:msg/FilterCloud.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__FILTER_CLOUD__STRUCT_H_
#define AID_ROBOT_MSGS__MSG__DETAIL__FILTER_CLOUD__STRUCT_H_

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
// Member 'filtered_points'
// Member 'raw_points'
#include "sensor_msgs/msg/detail/point_cloud2__struct.h"

/// Struct defined in msg/FilterCloud in the package aid_robot_msgs.
typedef struct aid_robot_msgs__msg__FilterCloud
{
  std_msgs__msg__Header header;
  sensor_msgs__msg__PointCloud2 filtered_points;
  sensor_msgs__msg__PointCloud2 raw_points;
} aid_robot_msgs__msg__FilterCloud;

// Struct for a sequence of aid_robot_msgs__msg__FilterCloud.
typedef struct aid_robot_msgs__msg__FilterCloud__Sequence
{
  aid_robot_msgs__msg__FilterCloud * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__msg__FilterCloud__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__FILTER_CLOUD__STRUCT_H_
