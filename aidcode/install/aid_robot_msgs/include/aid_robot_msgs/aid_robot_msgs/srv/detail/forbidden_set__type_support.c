// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aid_robot_msgs:srv/ForbiddenSet.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aid_robot_msgs/srv/detail/forbidden_set__rosidl_typesupport_introspection_c.h"
#include "aid_robot_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aid_robot_msgs/srv/detail/forbidden_set__functions.h"
#include "aid_robot_msgs/srv/detail/forbidden_set__struct.h"


// Include directives for member types
// Member `frame_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `lines`
#include "aid_robot_msgs/msg/start_to_end_point.h"
// Member `lines`
#include "aid_robot_msgs/msg/detail/start_to_end_point__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aid_robot_msgs__srv__ForbiddenSet_Request__init(message_memory);
}

void aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_fini_function(void * message_memory)
{
  aid_robot_msgs__srv__ForbiddenSet_Request__fini(message_memory);
}

size_t aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__size_function__ForbiddenSet_Request__lines(
  const void * untyped_member)
{
  const aid_robot_msgs__msg__StartToEndPoint__Sequence * member =
    (const aid_robot_msgs__msg__StartToEndPoint__Sequence *)(untyped_member);
  return member->size;
}

const void * aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__get_const_function__ForbiddenSet_Request__lines(
  const void * untyped_member, size_t index)
{
  const aid_robot_msgs__msg__StartToEndPoint__Sequence * member =
    (const aid_robot_msgs__msg__StartToEndPoint__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__get_function__ForbiddenSet_Request__lines(
  void * untyped_member, size_t index)
{
  aid_robot_msgs__msg__StartToEndPoint__Sequence * member =
    (aid_robot_msgs__msg__StartToEndPoint__Sequence *)(untyped_member);
  return &member->data[index];
}

void aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__fetch_function__ForbiddenSet_Request__lines(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const aid_robot_msgs__msg__StartToEndPoint * item =
    ((const aid_robot_msgs__msg__StartToEndPoint *)
    aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__get_const_function__ForbiddenSet_Request__lines(untyped_member, index));
  aid_robot_msgs__msg__StartToEndPoint * value =
    (aid_robot_msgs__msg__StartToEndPoint *)(untyped_value);
  *value = *item;
}

void aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__assign_function__ForbiddenSet_Request__lines(
  void * untyped_member, size_t index, const void * untyped_value)
{
  aid_robot_msgs__msg__StartToEndPoint * item =
    ((aid_robot_msgs__msg__StartToEndPoint *)
    aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__get_function__ForbiddenSet_Request__lines(untyped_member, index));
  const aid_robot_msgs__msg__StartToEndPoint * value =
    (const aid_robot_msgs__msg__StartToEndPoint *)(untyped_value);
  *item = *value;
}

bool aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__resize_function__ForbiddenSet_Request__lines(
  void * untyped_member, size_t size)
{
  aid_robot_msgs__msg__StartToEndPoint__Sequence * member =
    (aid_robot_msgs__msg__StartToEndPoint__Sequence *)(untyped_member);
  aid_robot_msgs__msg__StartToEndPoint__Sequence__fini(member);
  return aid_robot_msgs__msg__StartToEndPoint__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_message_member_array[3] = {
  {
    "map_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aid_robot_msgs__srv__ForbiddenSet_Request, map_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "frame_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aid_robot_msgs__srv__ForbiddenSet_Request, frame_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "lines",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aid_robot_msgs__srv__ForbiddenSet_Request, lines),  // bytes offset in struct
    NULL,  // default value
    aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__size_function__ForbiddenSet_Request__lines,  // size() function pointer
    aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__get_const_function__ForbiddenSet_Request__lines,  // get_const(index) function pointer
    aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__get_function__ForbiddenSet_Request__lines,  // get(index) function pointer
    aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__fetch_function__ForbiddenSet_Request__lines,  // fetch(index, &value) function pointer
    aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__assign_function__ForbiddenSet_Request__lines,  // assign(index, value) function pointer
    aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__resize_function__ForbiddenSet_Request__lines  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_message_members = {
  "aid_robot_msgs__srv",  // message namespace
  "ForbiddenSet_Request",  // message name
  3,  // number of fields
  sizeof(aid_robot_msgs__srv__ForbiddenSet_Request),
  aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_message_member_array,  // message members
  aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_message_type_support_handle = {
  0,
  &aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aid_robot_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aid_robot_msgs, srv, ForbiddenSet_Request)() {
  aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aid_robot_msgs, msg, StartToEndPoint)();
  if (!aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_message_type_support_handle.typesupport_identifier) {
    aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aid_robot_msgs__srv__ForbiddenSet_Request__rosidl_typesupport_introspection_c__ForbiddenSet_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aid_robot_msgs/srv/detail/forbidden_set__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aid_robot_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aid_robot_msgs/srv/detail/forbidden_set__functions.h"
// already included above
// #include "aid_robot_msgs/srv/detail/forbidden_set__struct.h"


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aid_robot_msgs__srv__ForbiddenSet_Response__init(message_memory);
}

void aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_fini_function(void * message_memory)
{
  aid_robot_msgs__srv__ForbiddenSet_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_message_member_array[2] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aid_robot_msgs__srv__ForbiddenSet_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aid_robot_msgs__srv__ForbiddenSet_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_message_members = {
  "aid_robot_msgs__srv",  // message namespace
  "ForbiddenSet_Response",  // message name
  2,  // number of fields
  sizeof(aid_robot_msgs__srv__ForbiddenSet_Response),
  aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_message_member_array,  // message members
  aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_message_type_support_handle = {
  0,
  &aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aid_robot_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aid_robot_msgs, srv, ForbiddenSet_Response)() {
  if (!aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_message_type_support_handle.typesupport_identifier) {
    aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aid_robot_msgs__srv__ForbiddenSet_Response__rosidl_typesupport_introspection_c__ForbiddenSet_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "aid_robot_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "aid_robot_msgs/srv/detail/forbidden_set__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers aid_robot_msgs__srv__detail__forbidden_set__rosidl_typesupport_introspection_c__ForbiddenSet_service_members = {
  "aid_robot_msgs__srv",  // service namespace
  "ForbiddenSet",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // aid_robot_msgs__srv__detail__forbidden_set__rosidl_typesupport_introspection_c__ForbiddenSet_Request_message_type_support_handle,
  NULL  // response message
  // aid_robot_msgs__srv__detail__forbidden_set__rosidl_typesupport_introspection_c__ForbiddenSet_Response_message_type_support_handle
};

static rosidl_service_type_support_t aid_robot_msgs__srv__detail__forbidden_set__rosidl_typesupport_introspection_c__ForbiddenSet_service_type_support_handle = {
  0,
  &aid_robot_msgs__srv__detail__forbidden_set__rosidl_typesupport_introspection_c__ForbiddenSet_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aid_robot_msgs, srv, ForbiddenSet_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aid_robot_msgs, srv, ForbiddenSet_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aid_robot_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aid_robot_msgs, srv, ForbiddenSet)() {
  if (!aid_robot_msgs__srv__detail__forbidden_set__rosidl_typesupport_introspection_c__ForbiddenSet_service_type_support_handle.typesupport_identifier) {
    aid_robot_msgs__srv__detail__forbidden_set__rosidl_typesupport_introspection_c__ForbiddenSet_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)aid_robot_msgs__srv__detail__forbidden_set__rosidl_typesupport_introspection_c__ForbiddenSet_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aid_robot_msgs, srv, ForbiddenSet_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aid_robot_msgs, srv, ForbiddenSet_Response)()->data;
  }

  return &aid_robot_msgs__srv__detail__forbidden_set__rosidl_typesupport_introspection_c__ForbiddenSet_service_type_support_handle;
}
