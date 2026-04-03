// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aid_robot_msgs:srv/FindBestVelocity.idl
// generated code does not contain a copyright notice
#include "aid_robot_msgs/srv/detail/find_best_velocity__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
aid_robot_msgs__srv__FindBestVelocity_Request__init(aid_robot_msgs__srv__FindBestVelocity_Request * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    aid_robot_msgs__srv__FindBestVelocity_Request__fini(msg);
    return false;
  }
  // max_angular_velocity
  // max_speed
  // len
  return true;
}

void
aid_robot_msgs__srv__FindBestVelocity_Request__fini(aid_robot_msgs__srv__FindBestVelocity_Request * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // max_angular_velocity
  // max_speed
  // len
}

bool
aid_robot_msgs__srv__FindBestVelocity_Request__are_equal(const aid_robot_msgs__srv__FindBestVelocity_Request * lhs, const aid_robot_msgs__srv__FindBestVelocity_Request * rhs)
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
  // max_angular_velocity
  if (lhs->max_angular_velocity != rhs->max_angular_velocity) {
    return false;
  }
  // max_speed
  if (lhs->max_speed != rhs->max_speed) {
    return false;
  }
  // len
  if (lhs->len != rhs->len) {
    return false;
  }
  return true;
}

bool
aid_robot_msgs__srv__FindBestVelocity_Request__copy(
  const aid_robot_msgs__srv__FindBestVelocity_Request * input,
  aid_robot_msgs__srv__FindBestVelocity_Request * output)
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
  // max_angular_velocity
  output->max_angular_velocity = input->max_angular_velocity;
  // max_speed
  output->max_speed = input->max_speed;
  // len
  output->len = input->len;
  return true;
}

aid_robot_msgs__srv__FindBestVelocity_Request *
aid_robot_msgs__srv__FindBestVelocity_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__FindBestVelocity_Request * msg = (aid_robot_msgs__srv__FindBestVelocity_Request *)allocator.allocate(sizeof(aid_robot_msgs__srv__FindBestVelocity_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aid_robot_msgs__srv__FindBestVelocity_Request));
  bool success = aid_robot_msgs__srv__FindBestVelocity_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aid_robot_msgs__srv__FindBestVelocity_Request__destroy(aid_robot_msgs__srv__FindBestVelocity_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aid_robot_msgs__srv__FindBestVelocity_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aid_robot_msgs__srv__FindBestVelocity_Request__Sequence__init(aid_robot_msgs__srv__FindBestVelocity_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__FindBestVelocity_Request * data = NULL;

  if (size) {
    data = (aid_robot_msgs__srv__FindBestVelocity_Request *)allocator.zero_allocate(size, sizeof(aid_robot_msgs__srv__FindBestVelocity_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aid_robot_msgs__srv__FindBestVelocity_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aid_robot_msgs__srv__FindBestVelocity_Request__fini(&data[i - 1]);
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
aid_robot_msgs__srv__FindBestVelocity_Request__Sequence__fini(aid_robot_msgs__srv__FindBestVelocity_Request__Sequence * array)
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
      aid_robot_msgs__srv__FindBestVelocity_Request__fini(&array->data[i]);
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

aid_robot_msgs__srv__FindBestVelocity_Request__Sequence *
aid_robot_msgs__srv__FindBestVelocity_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__FindBestVelocity_Request__Sequence * array = (aid_robot_msgs__srv__FindBestVelocity_Request__Sequence *)allocator.allocate(sizeof(aid_robot_msgs__srv__FindBestVelocity_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aid_robot_msgs__srv__FindBestVelocity_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aid_robot_msgs__srv__FindBestVelocity_Request__Sequence__destroy(aid_robot_msgs__srv__FindBestVelocity_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aid_robot_msgs__srv__FindBestVelocity_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aid_robot_msgs__srv__FindBestVelocity_Request__Sequence__are_equal(const aid_robot_msgs__srv__FindBestVelocity_Request__Sequence * lhs, const aid_robot_msgs__srv__FindBestVelocity_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aid_robot_msgs__srv__FindBestVelocity_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aid_robot_msgs__srv__FindBestVelocity_Request__Sequence__copy(
  const aid_robot_msgs__srv__FindBestVelocity_Request__Sequence * input,
  aid_robot_msgs__srv__FindBestVelocity_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aid_robot_msgs__srv__FindBestVelocity_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aid_robot_msgs__srv__FindBestVelocity_Request * data =
      (aid_robot_msgs__srv__FindBestVelocity_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aid_robot_msgs__srv__FindBestVelocity_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aid_robot_msgs__srv__FindBestVelocity_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aid_robot_msgs__srv__FindBestVelocity_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `cmd_vel`
#include "geometry_msgs/msg/detail/twist__functions.h"
// Member `msg`
#include "rosidl_runtime_c/string_functions.h"

bool
aid_robot_msgs__srv__FindBestVelocity_Response__init(aid_robot_msgs__srv__FindBestVelocity_Response * msg)
{
  if (!msg) {
    return false;
  }
  // cmd_vel
  if (!geometry_msgs__msg__Twist__init(&msg->cmd_vel)) {
    aid_robot_msgs__srv__FindBestVelocity_Response__fini(msg);
    return false;
  }
  // success
  // msg
  if (!rosidl_runtime_c__String__init(&msg->msg)) {
    aid_robot_msgs__srv__FindBestVelocity_Response__fini(msg);
    return false;
  }
  return true;
}

void
aid_robot_msgs__srv__FindBestVelocity_Response__fini(aid_robot_msgs__srv__FindBestVelocity_Response * msg)
{
  if (!msg) {
    return;
  }
  // cmd_vel
  geometry_msgs__msg__Twist__fini(&msg->cmd_vel);
  // success
  // msg
  rosidl_runtime_c__String__fini(&msg->msg);
}

bool
aid_robot_msgs__srv__FindBestVelocity_Response__are_equal(const aid_robot_msgs__srv__FindBestVelocity_Response * lhs, const aid_robot_msgs__srv__FindBestVelocity_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // cmd_vel
  if (!geometry_msgs__msg__Twist__are_equal(
      &(lhs->cmd_vel), &(rhs->cmd_vel)))
  {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // msg
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->msg), &(rhs->msg)))
  {
    return false;
  }
  return true;
}

bool
aid_robot_msgs__srv__FindBestVelocity_Response__copy(
  const aid_robot_msgs__srv__FindBestVelocity_Response * input,
  aid_robot_msgs__srv__FindBestVelocity_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // cmd_vel
  if (!geometry_msgs__msg__Twist__copy(
      &(input->cmd_vel), &(output->cmd_vel)))
  {
    return false;
  }
  // success
  output->success = input->success;
  // msg
  if (!rosidl_runtime_c__String__copy(
      &(input->msg), &(output->msg)))
  {
    return false;
  }
  return true;
}

aid_robot_msgs__srv__FindBestVelocity_Response *
aid_robot_msgs__srv__FindBestVelocity_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__FindBestVelocity_Response * msg = (aid_robot_msgs__srv__FindBestVelocity_Response *)allocator.allocate(sizeof(aid_robot_msgs__srv__FindBestVelocity_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aid_robot_msgs__srv__FindBestVelocity_Response));
  bool success = aid_robot_msgs__srv__FindBestVelocity_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aid_robot_msgs__srv__FindBestVelocity_Response__destroy(aid_robot_msgs__srv__FindBestVelocity_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aid_robot_msgs__srv__FindBestVelocity_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aid_robot_msgs__srv__FindBestVelocity_Response__Sequence__init(aid_robot_msgs__srv__FindBestVelocity_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__FindBestVelocity_Response * data = NULL;

  if (size) {
    data = (aid_robot_msgs__srv__FindBestVelocity_Response *)allocator.zero_allocate(size, sizeof(aid_robot_msgs__srv__FindBestVelocity_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aid_robot_msgs__srv__FindBestVelocity_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aid_robot_msgs__srv__FindBestVelocity_Response__fini(&data[i - 1]);
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
aid_robot_msgs__srv__FindBestVelocity_Response__Sequence__fini(aid_robot_msgs__srv__FindBestVelocity_Response__Sequence * array)
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
      aid_robot_msgs__srv__FindBestVelocity_Response__fini(&array->data[i]);
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

aid_robot_msgs__srv__FindBestVelocity_Response__Sequence *
aid_robot_msgs__srv__FindBestVelocity_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__FindBestVelocity_Response__Sequence * array = (aid_robot_msgs__srv__FindBestVelocity_Response__Sequence *)allocator.allocate(sizeof(aid_robot_msgs__srv__FindBestVelocity_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aid_robot_msgs__srv__FindBestVelocity_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aid_robot_msgs__srv__FindBestVelocity_Response__Sequence__destroy(aid_robot_msgs__srv__FindBestVelocity_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aid_robot_msgs__srv__FindBestVelocity_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aid_robot_msgs__srv__FindBestVelocity_Response__Sequence__are_equal(const aid_robot_msgs__srv__FindBestVelocity_Response__Sequence * lhs, const aid_robot_msgs__srv__FindBestVelocity_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aid_robot_msgs__srv__FindBestVelocity_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aid_robot_msgs__srv__FindBestVelocity_Response__Sequence__copy(
  const aid_robot_msgs__srv__FindBestVelocity_Response__Sequence * input,
  aid_robot_msgs__srv__FindBestVelocity_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aid_robot_msgs__srv__FindBestVelocity_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aid_robot_msgs__srv__FindBestVelocity_Response * data =
      (aid_robot_msgs__srv__FindBestVelocity_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aid_robot_msgs__srv__FindBestVelocity_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aid_robot_msgs__srv__FindBestVelocity_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aid_robot_msgs__srv__FindBestVelocity_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
