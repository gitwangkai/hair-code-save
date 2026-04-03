// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aid_robot_msgs:msg/AidPose.idl
// generated code does not contain a copyright notice
#include "aid_robot_msgs/msg/detail/aid_pose__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `name`
#include "rosidl_runtime_c/string_functions.h"

bool
aid_robot_msgs__msg__AidPose__init(aid_robot_msgs__msg__AidPose * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    aid_robot_msgs__msg__AidPose__fini(msg);
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    aid_robot_msgs__msg__AidPose__fini(msg);
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    aid_robot_msgs__msg__AidPose__fini(msg);
    return false;
  }
  return true;
}

void
aid_robot_msgs__msg__AidPose__fini(aid_robot_msgs__msg__AidPose * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // name
  rosidl_runtime_c__String__fini(&msg->name);
}

bool
aid_robot_msgs__msg__AidPose__are_equal(const aid_robot_msgs__msg__AidPose * lhs, const aid_robot_msgs__msg__AidPose * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->name), &(rhs->name)))
  {
    return false;
  }
  return true;
}

bool
aid_robot_msgs__msg__AidPose__copy(
  const aid_robot_msgs__msg__AidPose * input,
  aid_robot_msgs__msg__AidPose * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__copy(
      &(input->name), &(output->name)))
  {
    return false;
  }
  return true;
}

aid_robot_msgs__msg__AidPose *
aid_robot_msgs__msg__AidPose__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__AidPose * msg = (aid_robot_msgs__msg__AidPose *)allocator.allocate(sizeof(aid_robot_msgs__msg__AidPose), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aid_robot_msgs__msg__AidPose));
  bool success = aid_robot_msgs__msg__AidPose__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aid_robot_msgs__msg__AidPose__destroy(aid_robot_msgs__msg__AidPose * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aid_robot_msgs__msg__AidPose__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aid_robot_msgs__msg__AidPose__Sequence__init(aid_robot_msgs__msg__AidPose__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__AidPose * data = NULL;

  if (size) {
    data = (aid_robot_msgs__msg__AidPose *)allocator.zero_allocate(size, sizeof(aid_robot_msgs__msg__AidPose), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aid_robot_msgs__msg__AidPose__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aid_robot_msgs__msg__AidPose__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aid_robot_msgs__msg__AidPose__Sequence__fini(aid_robot_msgs__msg__AidPose__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aid_robot_msgs__msg__AidPose__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aid_robot_msgs__msg__AidPose__Sequence *
aid_robot_msgs__msg__AidPose__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__AidPose__Sequence * array = (aid_robot_msgs__msg__AidPose__Sequence *)allocator.allocate(sizeof(aid_robot_msgs__msg__AidPose__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aid_robot_msgs__msg__AidPose__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aid_robot_msgs__msg__AidPose__Sequence__destroy(aid_robot_msgs__msg__AidPose__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aid_robot_msgs__msg__AidPose__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aid_robot_msgs__msg__AidPose__Sequence__are_equal(const aid_robot_msgs__msg__AidPose__Sequence * lhs, const aid_robot_msgs__msg__AidPose__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aid_robot_msgs__msg__AidPose__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aid_robot_msgs__msg__AidPose__Sequence__copy(
  const aid_robot_msgs__msg__AidPose__Sequence * input,
  aid_robot_msgs__msg__AidPose__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aid_robot_msgs__msg__AidPose);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aid_robot_msgs__msg__AidPose * data =
      (aid_robot_msgs__msg__AidPose *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aid_robot_msgs__msg__AidPose__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aid_robot_msgs__msg__AidPose__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aid_robot_msgs__msg__AidPose__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
