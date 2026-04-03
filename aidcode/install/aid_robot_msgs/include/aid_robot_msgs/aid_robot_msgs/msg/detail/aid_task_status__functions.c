// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aid_robot_msgs:msg/AidTaskStatus.idl
// generated code does not contain a copyright notice
#include "aid_robot_msgs/msg/detail/aid_task_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
aid_robot_msgs__msg__AidTaskStatus__init(aid_robot_msgs__msg__AidTaskStatus * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // task_type
  return true;
}

void
aid_robot_msgs__msg__AidTaskStatus__fini(aid_robot_msgs__msg__AidTaskStatus * msg)
{
  if (!msg) {
    return;
  }
  // status
  // task_type
}

bool
aid_robot_msgs__msg__AidTaskStatus__are_equal(const aid_robot_msgs__msg__AidTaskStatus * lhs, const aid_robot_msgs__msg__AidTaskStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // task_type
  if (lhs->task_type != rhs->task_type) {
    return false;
  }
  return true;
}

bool
aid_robot_msgs__msg__AidTaskStatus__copy(
  const aid_robot_msgs__msg__AidTaskStatus * input,
  aid_robot_msgs__msg__AidTaskStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // task_type
  output->task_type = input->task_type;
  return true;
}

aid_robot_msgs__msg__AidTaskStatus *
aid_robot_msgs__msg__AidTaskStatus__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__AidTaskStatus * msg = (aid_robot_msgs__msg__AidTaskStatus *)allocator.allocate(sizeof(aid_robot_msgs__msg__AidTaskStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aid_robot_msgs__msg__AidTaskStatus));
  bool success = aid_robot_msgs__msg__AidTaskStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aid_robot_msgs__msg__AidTaskStatus__destroy(aid_robot_msgs__msg__AidTaskStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aid_robot_msgs__msg__AidTaskStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aid_robot_msgs__msg__AidTaskStatus__Sequence__init(aid_robot_msgs__msg__AidTaskStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__AidTaskStatus * data = NULL;

  if (size) {
    data = (aid_robot_msgs__msg__AidTaskStatus *)allocator.zero_allocate(size, sizeof(aid_robot_msgs__msg__AidTaskStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aid_robot_msgs__msg__AidTaskStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aid_robot_msgs__msg__AidTaskStatus__fini(&data[i - 1]);
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
aid_robot_msgs__msg__AidTaskStatus__Sequence__fini(aid_robot_msgs__msg__AidTaskStatus__Sequence * array)
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
      aid_robot_msgs__msg__AidTaskStatus__fini(&array->data[i]);
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

aid_robot_msgs__msg__AidTaskStatus__Sequence *
aid_robot_msgs__msg__AidTaskStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__AidTaskStatus__Sequence * array = (aid_robot_msgs__msg__AidTaskStatus__Sequence *)allocator.allocate(sizeof(aid_robot_msgs__msg__AidTaskStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aid_robot_msgs__msg__AidTaskStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aid_robot_msgs__msg__AidTaskStatus__Sequence__destroy(aid_robot_msgs__msg__AidTaskStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aid_robot_msgs__msg__AidTaskStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aid_robot_msgs__msg__AidTaskStatus__Sequence__are_equal(const aid_robot_msgs__msg__AidTaskStatus__Sequence * lhs, const aid_robot_msgs__msg__AidTaskStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aid_robot_msgs__msg__AidTaskStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aid_robot_msgs__msg__AidTaskStatus__Sequence__copy(
  const aid_robot_msgs__msg__AidTaskStatus__Sequence * input,
  aid_robot_msgs__msg__AidTaskStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aid_robot_msgs__msg__AidTaskStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aid_robot_msgs__msg__AidTaskStatus * data =
      (aid_robot_msgs__msg__AidTaskStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aid_robot_msgs__msg__AidTaskStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aid_robot_msgs__msg__AidTaskStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aid_robot_msgs__msg__AidTaskStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
