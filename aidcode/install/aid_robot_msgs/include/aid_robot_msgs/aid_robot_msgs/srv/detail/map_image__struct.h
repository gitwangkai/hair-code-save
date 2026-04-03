// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aid_robot_msgs:srv/MapImage.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__MAP_IMAGE__STRUCT_H_
#define AID_ROBOT_MSGS__SRV__DETAIL__MAP_IMAGE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/MapImage in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__MapImage_Request
{
  uint32_t id;
} aid_robot_msgs__srv__MapImage_Request;

// Struct for a sequence of aid_robot_msgs__srv__MapImage_Request.
typedef struct aid_robot_msgs__srv__MapImage_Request__Sequence
{
  aid_robot_msgs__srv__MapImage_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__MapImage_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'map'
#include "nav_msgs/msg/detail/occupancy_grid__struct.h"
// Member 'map_file'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MapImage in the package aid_robot_msgs.
typedef struct aid_robot_msgs__srv__MapImage_Response
{
  bool success;
  nav_msgs__msg__OccupancyGrid map;
  rosidl_runtime_c__String map_file;
} aid_robot_msgs__srv__MapImage_Response;

// Struct for a sequence of aid_robot_msgs__srv__MapImage_Response.
typedef struct aid_robot_msgs__srv__MapImage_Response__Sequence
{
  aid_robot_msgs__srv__MapImage_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aid_robot_msgs__srv__MapImage_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__MAP_IMAGE__STRUCT_H_
