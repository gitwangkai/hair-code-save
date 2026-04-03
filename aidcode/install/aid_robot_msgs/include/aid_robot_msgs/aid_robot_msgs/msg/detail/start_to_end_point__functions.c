// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aid_robot_msgs:msg/StartToEndPoint.idl
// generated code does not contain a copyright notice
#include "aid_robot_msgs/msg/detail/start_to_end_point__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `start`
// Member `end`
#include "geometry_msgs/msg/detail/point32__functions.h"

bool
aid_robot_msgs__msg__StartToEndPoint__init(aid_robot_msgs__msg__StartToEndPoint * msg)
{
  if (!msg) {
    return false;
  }
  // start
  if (!geometry_msgs__msg__Point32__init(&msg->start)) {
    aid_robot_msgs__msg__StartToEndPoint__fini(msg);
    return false;
  }
  // end
  if (!geometry_msgs__msg__Point32__init(&msg->end)) {
    aid_robot_msgs__msg__StartToEndPoint__fini(msg);
    return false;
  }
  return true;
}

void
aid_robot_msgs__msg__StartToEndPoint__fini(aid_robot_msgs__msg__StartToEndPoint * msg)
{
  if (!msg) {
    return;
  }
  // start
  geometry_msgs__msg__Point32__fini(&msg->start);
  // end
  geometry_msgs__msg__Point32__fini(&msg->end);
}

bool
aid_robot_msgs__msg__StartToEndPoint__are_equal(const aid_robot_msgs__msg__StartToEndPoint * lhs, const aid_robot_msgs__msg__StartToEndPoint * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // start
  if (!geometry_msgs__msg__Point32__are_equal(
      &(lhs->start), &(rhs->start)))
  {
    return false;
  }
  // end
  if (!geometry_msgs__msg__Point32__are_equal(
      &(lhs->end), &(rhs->end)))
  {
    return false;
  }
  return true;
}

bool
aid_robot_msgs__msg__StartToEndPoint__copy(
  const aid_robot_msgs__msg__StartToEndPoint * input,
  aid_robot_msgs__msg__StartToEndPoint * output)
{
  if (!input || !output) {
    return false;
  }
  // start
  if (!geometry_msgs__msg__Point32__copy(
      &(input->start), &(output->start)))
  {
    return false;
  }
  // end
  if (!geometry_msgs__msg__Point32__copy(
      &(input->end), &(output->end)))
  {
    return false;
  }
  return true;
}

aid_robot_msgs__msg__StartToEndPoint *
aid_robot_msgs__msg__StartToEndPoint__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__StartToEndPoint * msg = (aid_robot_msgs__msg__StartToEndPoint *)allocator.allocate(sizeof(aid_robot_msgs__msg__StartToEndPoint), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aid_robot_msgs__msg__StartToEndPoint));
  bool success = aid_robot_msgs__msg__StartToEndPoint__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aid_robot_msgs__msg__StartToEndPoint__destroy(aid_robot_msgs__msg__StartToEndPoint * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aid_robot_msgs__msg__StartToEndPoint__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aid_robot_msgs__msg__StartToEndPoint__Sequence__init(aid_robot_msgs__msg__StartToEndPoint__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__StartToEndPoint * data = NULL;

  if (size) {
    data = (aid_robot_msgs__msg__StartToEndPoint *)allocator.zero_allocate(size, sizeof(aid_robot_msgs__msg__StartToEndPoint), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aid_robot_msgs__msg__StartToEndPoint__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aid_robot_msgs__msg__StartToEndPoint__fini(&data[i - 1]);
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
aid_robot_msgs__msg__StartToEndPoint__Sequence__fini(aid_robot_msgs__msg__StartToEndPoint__Sequence * array)
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
      aid_robot_msgs__msg__StartToEndPoint__fini(&array->data[i]);
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

aid_robot_msgs__msg__StartToEndPoint__Sequence *
aid_robot_msgs__msg__StartToEndPoint__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__StartToEndPoint__Sequence * array = (aid_robot_msgs__msg__StartToEndPoint__Sequence *)allocator.allocate(sizeof(aid_robot_msgs__msg__StartToEndPoint__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aid_robot_msgs__msg__StartToEndPoint__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aid_robot_msgs__msg__StartToEndPoint__Sequence__destroy(aid_robot_msgs__msg__StartToEndPoint__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aid_robot_msgs__msg__StartToEndPoint__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aid_robot_msgs__msg__StartToEndPoint__Sequence__are_equal(const aid_robot_msgs__msg__StartToEndPoint__Sequence * lhs, const aid_robot_msgs__msg__StartToEndPoint__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aid_robot_msgs__msg__StartToEndPoint__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aid_robot_msgs__msg__StartToEndPoint__Sequence__copy(
  const aid_robot_msgs__msg__StartToEndPoint__Sequence * input,
  aid_robot_msgs__msg__StartToEndPoint__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aid_robot_msgs__msg__StartToEndPoint);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aid_robot_msgs__msg__StartToEndPoint * data =
      (aid_robot_msgs__msg__StartToEndPoint *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aid_robot_msgs__msg__StartToEndPoint__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aid_robot_msgs__msg__StartToEndPoint__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aid_robot_msgs__msg__StartToEndPoint__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
