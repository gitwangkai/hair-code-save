// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:msg/AidTaskStatus.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__STRUCT_H_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/AidTaskStatus in the package aid_robot_msgs.
typedef struct aid_robot_msgs__msg__AidTaskStatus
{
  /// 0:idle 1:working 2:success 3:failed 4 suspend 5:cancle
  int32_t status;
  /// 0:单点 1:巡视
  int32_t task_type;
} aid_robot_msgs__msg__AidTaskStatus;

// Struct for a sequence of aid_robot_msgs__msg__AidTaskStatus.
typedef struct aid_robot_msgs__msg__AidTaskStatus__Sequence
{
  aid_robot_msgs__msg__AidTaskStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__msg__AidTaskStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__STRUCT_H_
