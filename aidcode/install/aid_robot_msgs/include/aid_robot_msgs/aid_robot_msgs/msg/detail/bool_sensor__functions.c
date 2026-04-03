// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aid_robot_msgs:msg/BoolSensor.idl
// generated code does not contain a copyright notice
#include "aid_robot_msgs/msg/detail/bool_sensor__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
aid_robot_msgs__msg__BoolSensor__init(aid_robot_msgs__msg__BoolSensor * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    aid_robot_msgs__msg__BoolSensor__fini(msg);
    return false;
  }
  // triggered
  return true;
}

void
aid_robot_msgs__msg__BoolSensor__fini(aid_robot_msgs__msg__BoolSensor * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // triggered
}

bool
aid_robot_msgs__msg__BoolSensor__are_equal(const aid_robot_msgs__msg__BoolSensor * lhs, const aid_robot_msgs__msg__BoolSensor * rhs)
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
  // triggered
  if (lhs->triggered != rhs->triggered) {
    return false;
  }
  return true;
}

bool
aid_robot_msgs__msg__BoolSensor__copy(
  const aid_robot_msgs__msg__BoolSensor * input,
  aid_robot_msgs__msg__BoolSensor * output)
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
  // triggered
  output->triggered = input->triggered;
  return true;
}

aid_robot_msgs__msg__BoolSensor *
aid_robot_msgs__msg__BoolSensor__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__BoolSensor * msg = (aid_robot_msgs__msg__BoolSensor *)allocator.allocate(sizeof(aid_robot_msgs__msg__BoolSensor), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aid_robot_msgs__msg__BoolSensor));
  bool success = aid_robot_msgs__msg__BoolSensor__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aid_robot_msgs__msg__BoolSensor__destroy(aid_robot_msgs__msg__BoolSensor * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aid_robot_msgs__msg__BoolSensor__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aid_robot_msgs__msg__BoolSensor__Sequence__init(aid_robot_msgs__msg__BoolSensor__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__BoolSensor * data = NULL;

  if (size) {
    data = (aid_robot_msgs__msg__BoolSensor *)allocator.zero_allocate(size, sizeof(aid_robot_msgs__msg__BoolSensor), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aid_robot_msgs__msg__BoolSensor__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aid_robot_msgs__msg__BoolSensor__fini(&data[i - 1]);
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
aid_robot_msgs__msg__BoolSensor__Sequence__fini(aid_robot_msgs__msg__BoolSensor__Sequence * array)
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
      aid_robot_msgs__msg__BoolSensor__fini(&array->data[i]);
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

aid_robot_msgs__msg__BoolSensor__Sequence *
aid_robot_msgs__msg__BoolSensor__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__BoolSensor__Sequence * array = (aid_robot_msgs__msg__BoolSensor__Sequence *)allocator.allocate(sizeof(aid_robot_msgs__msg__BoolSensor__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aid_robot_msgs__msg__BoolSensor__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aid_robot_msgs__msg__BoolSensor__Sequence__destroy(aid_robot_msgs__msg__BoolSensor__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aid_robot_msgs__msg__BoolSensor__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aid_robot_msgs__msg__BoolSensor__Sequence__are_equal(const aid_robot_msgs__msg__BoolSensor__Sequence * lhs, const aid_robot_msgs__msg__BoolSensor__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aid_robot_msgs__msg__BoolSensor__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aid_robot_msgs__msg__BoolSensor__Sequence__copy(
  const aid_robot_msgs__msg__BoolSensor__Sequence * input,
  aid_robot_msgs__msg__BoolSensor__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aid_robot_msgs__msg__BoolSensor);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aid_robot_msgs__msg__BoolSensor * data =
      (aid_robot_msgs__msg__BoolSensor *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aid_robot_msgs__msg__BoolSensor__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aid_robot_msgs__msg__BoolSensor__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aid_robot_msgs__msg__BoolSensor__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
