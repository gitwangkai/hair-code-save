// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aid_robot_msgs:srv/PoseNav.idl
// generated code does not contain a copyright notice
#include "aid_robot_msgs/srv/detail/pose_nav__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/detail/pose_stamped__functions.h"

bool
aid_robot_msgs__srv__PoseNav_Request__init(aid_robot_msgs__srv__PoseNav_Request * msg)
{
  if (!msg) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__PoseStamped__init(&msg->pose)) {
    aid_robot_msgs__srv__PoseNav_Request__fini(msg);
    return false;
  }
  return true;
}

void
aid_robot_msgs__srv__PoseNav_Request__fini(aid_robot_msgs__srv__PoseNav_Request * msg)
{
  if (!msg) {
    return;
  }
  // pose
  geometry_msgs__msg__PoseStamped__fini(&msg->pose);
}

bool
aid_robot_msgs__srv__PoseNav_Request__are_equal(const aid_robot_msgs__srv__PoseNav_Request * lhs, const aid_robot_msgs__srv__PoseNav_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__PoseStamped__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  return true;
}

bool
aid_robot_msgs__srv__PoseNav_Request__copy(
  const aid_robot_msgs__srv__PoseNav_Request * input,
  aid_robot_msgs__srv__PoseNav_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__PoseStamped__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  return true;
}

aid_robot_msgs__srv__PoseNav_Request *
aid_robot_msgs__srv__PoseNav_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__PoseNav_Request * msg = (aid_robot_msgs__srv__PoseNav_Request *)allocator.allocate(sizeof(aid_robot_msgs__srv__PoseNav_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aid_robot_msgs__srv__PoseNav_Request));
  bool success = aid_robot_msgs__srv__PoseNav_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aid_robot_msgs__srv__PoseNav_Request__destroy(aid_robot_msgs__srv__PoseNav_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aid_robot_msgs__srv__PoseNav_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aid_robot_msgs__srv__PoseNav_Request__Sequence__init(aid_robot_msgs__srv__PoseNav_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__PoseNav_Request * data = NULL;

  if (size) {
    data = (aid_robot_msgs__srv__PoseNav_Request *)allocator.zero_allocate(size, sizeof(aid_robot_msgs__srv__PoseNav_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aid_robot_msgs__srv__PoseNav_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aid_robot_msgs__srv__PoseNav_Request__fini(&data[i - 1]);
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
aid_robot_msgs__srv__PoseNav_Request__Sequence__fini(aid_robot_msgs__srv__PoseNav_Request__Sequence * array)
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
      aid_robot_msgs__srv__PoseNav_Request__fini(&array->data[i]);
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

aid_robot_msgs__srv__PoseNav_Request__Sequence *
aid_robot_msgs__srv__PoseNav_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__PoseNav_Request__Sequence * array = (aid_robot_msgs__srv__PoseNav_Request__Sequence *)allocator.allocate(sizeof(aid_robot_msgs__srv__PoseNav_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aid_robot_msgs__srv__PoseNav_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aid_robot_msgs__srv__PoseNav_Request__Sequence__destroy(aid_robot_msgs__srv__PoseNav_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aid_robot_msgs__srv__PoseNav_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aid_robot_msgs__srv__PoseNav_Request__Sequence__are_equal(const aid_robot_msgs__srv__PoseNav_Request__Sequence * lhs, const aid_robot_msgs__srv__PoseNav_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aid_robot_msgs__srv__PoseNav_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aid_robot_msgs__srv__PoseNav_Request__Sequence__copy(
  const aid_robot_msgs__srv__PoseNav_Request__Sequence * input,
  aid_robot_msgs__srv__PoseNav_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aid_robot_msgs__srv__PoseNav_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aid_robot_msgs__srv__PoseNav_Request * data =
      (aid_robot_msgs__srv__PoseNav_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aid_robot_msgs__srv__PoseNav_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aid_robot_msgs__srv__PoseNav_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aid_robot_msgs__srv__PoseNav_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
aid_robot_msgs__srv__PoseNav_Response__init(aid_robot_msgs__srv__PoseNav_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    aid_robot_msgs__srv__PoseNav_Response__fini(msg);
    return false;
  }
  return true;
}

void
aid_robot_msgs__srv__PoseNav_Response__fini(aid_robot_msgs__srv__PoseNav_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
aid_robot_msgs__srv__PoseNav_Response__are_equal(const aid_robot_msgs__srv__PoseNav_Response * lhs, const aid_robot_msgs__srv__PoseNav_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
aid_robot_msgs__srv__PoseNav_Response__copy(
  const aid_robot_msgs__srv__PoseNav_Response * input,
  aid_robot_msgs__srv__PoseNav_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

aid_robot_msgs__srv__PoseNav_Response *
aid_robot_msgs__srv__PoseNav_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__PoseNav_Response * msg = (aid_robot_msgs__srv__PoseNav_Response *)allocator.allocate(sizeof(aid_robot_msgs__srv__PoseNav_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aid_robot_msgs__srv__PoseNav_Response));
  bool success = aid_robot_msgs__srv__PoseNav_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aid_robot_msgs__srv__PoseNav_Response__destroy(aid_robot_msgs__srv__PoseNav_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aid_robot_msgs__srv__PoseNav_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aid_robot_msgs__srv__PoseNav_Response__Sequence__init(aid_robot_msgs__srv__PoseNav_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__PoseNav_Response * data = NULL;

  if (size) {
    data = (aid_robot_msgs__srv__PoseNav_Response *)allocator.zero_allocate(size, sizeof(aid_robot_msgs__srv__PoseNav_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aid_robot_msgs__srv__PoseNav_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aid_robot_msgs__srv__PoseNav_Response__fini(&data[i - 1]);
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
aid_robot_msgs__srv__PoseNav_Response__Sequence__fini(aid_robot_msgs__srv__PoseNav_Response__Sequence * array)
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
      aid_robot_msgs__srv__PoseNav_Response__fini(&array->data[i]);
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

aid_robot_msgs__srv__PoseNav_Response__Sequence *
aid_robot_msgs__srv__PoseNav_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__srv__PoseNav_Response__Sequence * array = (aid_robot_msgs__srv__PoseNav_Response__Sequence *)allocator.allocate(sizeof(aid_robot_msgs__srv__PoseNav_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aid_robot_msgs__srv__PoseNav_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aid_robot_msgs__srv__PoseNav_Response__Sequence__destroy(aid_robot_msgs__srv__PoseNav_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aid_robot_msgs__srv__PoseNav_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aid_robot_msgs__srv__PoseNav_Response__Sequence__are_equal(const aid_robot_msgs__srv__PoseNav_Response__Sequence * lhs, const aid_robot_msgs__srv__PoseNav_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aid_robot_msgs__srv__PoseNav_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aid_robot_msgs__srv__PoseNav_Response__Sequence__copy(
  const aid_robot_msgs__srv__PoseNav_Response__Sequence * input,
  aid_robot_msgs__srv__PoseNav_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aid_robot_msgs__srv__PoseNav_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aid_robot_msgs__srv__PoseNav_Response * data =
      (aid_robot_msgs__srv__PoseNav_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aid_robot_msgs__srv__PoseNav_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aid_robot_msgs__srv__PoseNav_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aid_robot_msgs__srv__PoseNav_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
