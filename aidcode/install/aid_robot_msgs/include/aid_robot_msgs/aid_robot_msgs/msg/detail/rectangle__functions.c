// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aid_robot_msgs:msg/Rectangle.idl
// generated code does not contain a copyright notice
#include "aid_robot_msgs/msg/detail/rectangle__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `center_point`
#include "geometry_msgs/msg/detail/point32__functions.h"

bool
aid_robot_msgs__msg__Rectangle__init(aid_robot_msgs__msg__Rectangle * msg)
{
  if (!msg) {
    return false;
  }
  // center_point
  if (!geometry_msgs__msg__Point32__init(&msg->center_point)) {
    aid_robot_msgs__msg__Rectangle__fini(msg);
    return false;
  }
  // side_length
  // grayscale
  return true;
}

void
aid_robot_msgs__msg__Rectangle__fini(aid_robot_msgs__msg__Rectangle * msg)
{
  if (!msg) {
    return;
  }
  // center_point
  geometry_msgs__msg__Point32__fini(&msg->center_point);
  // side_length
  // grayscale
}

bool
aid_robot_msgs__msg__Rectangle__are_equal(const aid_robot_msgs__msg__Rectangle * lhs, const aid_robot_msgs__msg__Rectangle * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // center_point
  if (!geometry_msgs__msg__Point32__are_equal(
      &(lhs->center_point), &(rhs->center_point)))
  {
    return false;
  }
  // side_length
  if (lhs->side_length != rhs->side_length) {
    return false;
  }
  // grayscale
  if (lhs->grayscale != rhs->grayscale) {
    return false;
  }
  return true;
}

bool
aid_robot_msgs__msg__Rectangle__copy(
  const aid_robot_msgs__msg__Rectangle * input,
  aid_robot_msgs__msg__Rectangle * output)
{
  if (!input || !output) {
    return false;
  }
  // center_point
  if (!geometry_msgs__msg__Point32__copy(
      &(input->center_point), &(output->center_point)))
  {
    return false;
  }
  // side_length
  output->side_length = input->side_length;
  // grayscale
  output->grayscale = input->grayscale;
  return true;
}

aid_robot_msgs__msg__Rectangle *
aid_robot_msgs__msg__Rectangle__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__Rectangle * msg = (aid_robot_msgs__msg__Rectangle *)allocator.allocate(sizeof(aid_robot_msgs__msg__Rectangle), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aid_robot_msgs__msg__Rectangle));
  bool success = aid_robot_msgs__msg__Rectangle__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aid_robot_msgs__msg__Rectangle__destroy(aid_robot_msgs__msg__Rectangle * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aid_robot_msgs__msg__Rectangle__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aid_robot_msgs__msg__Rectangle__Sequence__init(aid_robot_msgs__msg__Rectangle__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__Rectangle * data = NULL;

  if (size) {
    data = (aid_robot_msgs__msg__Rectangle *)allocator.zero_allocate(size, sizeof(aid_robot_msgs__msg__Rectangle), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aid_robot_msgs__msg__Rectangle__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aid_robot_msgs__msg__Rectangle__fini(&data[i - 1]);
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
aid_robot_msgs__msg__Rectangle__Sequence__fini(aid_robot_msgs__msg__Rectangle__Sequence * array)
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
      aid_robot_msgs__msg__Rectangle__fini(&array->data[i]);
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

aid_robot_msgs__msg__Rectangle__Sequence *
aid_robot_msgs__msg__Rectangle__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__Rectangle__Sequence * array = (aid_robot_msgs__msg__Rectangle__Sequence *)allocator.allocate(sizeof(aid_robot_msgs__msg__Rectangle__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aid_robot_msgs__msg__Rectangle__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aid_robot_msgs__msg__Rectangle__Sequence__destroy(aid_robot_msgs__msg__Rectangle__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aid_robot_msgs__msg__Rectangle__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aid_robot_msgs__msg__Rectangle__Sequence__are_equal(const aid_robot_msgs__msg__Rectangle__Sequence * lhs, const aid_robot_msgs__msg__Rectangle__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aid_robot_msgs__msg__Rectangle__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aid_robot_msgs__msg__Rectangle__Sequence__copy(
  const aid_robot_msgs__msg__Rectangle__Sequence * input,
  aid_robot_msgs__msg__Rectangle__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aid_robot_msgs__msg__Rectangle);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aid_robot_msgs__msg__Rectangle * data =
      (aid_robot_msgs__msg__Rectangle *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aid_robot_msgs__msg__Rectangle__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aid_robot_msgs__msg__Rectangle__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aid_robot_msgs__msg__Rectangle__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
