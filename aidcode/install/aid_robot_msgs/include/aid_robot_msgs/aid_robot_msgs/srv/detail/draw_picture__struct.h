// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:srv/DrawPicture.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__DRAW_PICTURE__STRUCT_H_
#define AID_ROBOT_MSGS__SRV__DETAIL__DRAW_PICTURE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'frame_id'
// Member 'type'
#include "rosidl_runtime_c/string.h"
// Member 'data'
#include "aid_robot_msgs/msg/detail/start_to_end_point__struct.h"
// Member 'rectangle_array'
#include "aid_robot_msgs/msg/detail/rectangle__struct.h"

/// Struct defined in srv/DrawPicture in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__DrawPicture_Request
{
  rosidl_runtime_c__String frame_id;
  rosidl_runtime_c__String type;
  uint32_t map_id;
  aid_robot_msgs__msg__StartToEndPoint__Sequence data;
  aid_robot_msgs__msg__Rectangle__Sequence rectangle_array;
} aid_robot_msgs__srv__DrawPicture_Request;

// Struct for a sequence of aid_robot_msgs__srv__DrawPicture_Request.
typedef struct aid_robot_msgs__srv__DrawPicture_Request__Sequence
{
  aid_robot_msgs__srv__DrawPicture_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__DrawPicture_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/DrawPicture in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__DrawPicture_Response
{
  bool success;
  rosidl_runtime_c__String message;
} aid_robot_msgs__srv__DrawPicture_Response;

// Struct for a sequence of aid_robot_msgs__srv__DrawPicture_Response.
typedef struct aid_robot_msgs__srv__DrawPicture_Response__Sequence
{
  aid_robot_msgs__srv__DrawPicture_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__DrawPicture_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__DRAW_PICTURE__STRUCT_H_
