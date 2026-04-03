// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aid_robot_msgs:msg/FilterCloud.idl
// generated code does not contain a copyright notice
#include "aid_robot_msgs/msg/detail/filter_cloud__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `filtered_points`
// Member `raw_points`
#include "sensor_msgs/msg/detail/point_cloud2__functions.h"

bool
aid_robot_msgs__msg__FilterCloud__init(aid_robot_msgs__msg__FilterCloud * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    aid_robot_msgs__msg__FilterCloud__fini(msg);
    return false;
  }
  // filtered_points
  if (!sensor_msgs__msg__PointCloud2__init(&msg->filtered_points)) {
    aid_robot_msgs__msg__FilterCloud__fini(msg);
    return false;
  }
  // raw_points
  if (!sensor_msgs__msg__PointCloud2__init(&msg->raw_points)) {
    aid_robot_msgs__msg__FilterCloud__fini(msg);
    return false;
  }
  return true;
}

void
aid_robot_msgs__msg__FilterCloud__fini(aid_robot_msgs__msg__FilterCloud * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // filtered_points
  sensor_msgs__msg__PointCloud2__fini(&msg->filtered_points);
  // raw_points
  sensor_msgs__msg__PointCloud2__fini(&msg->raw_points);
}

bool
aid_robot_msgs__msg__FilterCloud__are_equal(const aid_robot_msgs__msg__FilterCloud * lhs, const aid_robot_msgs__msg__FilterCloud * rhs)
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
  // filtered_points
  if (!sensor_msgs__msg__PointCloud2__are_equal(
      &(lhs->filtered_points), &(rhs->filtered_points)))
  {
    return false;
  }
  // raw_points
  if (!sensor_msgs__msg__PointCloud2__are_equal(
      &(lhs->raw_points), &(rhs->raw_points)))
  {
    return false;
  }
  return true;
}

bool
aid_robot_msgs__msg__FilterCloud__copy(
  const aid_robot_msgs__msg__FilterCloud * input,
  aid_robot_msgs__msg__FilterCloud * output)
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
  // filtered_points
  if (!sensor_msgs__msg__PointCloud2__copy(
      &(input->filtered_points), &(output->filtered_points)))
  {
    return false;
  }
  // raw_points
  if (!sensor_msgs__msg__PointCloud2__copy(
      &(input->raw_points), &(output->raw_points)))
  {
    return false;
  }
  return true;
}

aid_robot_msgs__msg__FilterCloud *
aid_robot_msgs__msg__FilterCloud__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__FilterCloud * msg = (aid_robot_msgs__msg__FilterCloud *)allocator.allocate(sizeof(aid_robot_msgs__msg__FilterCloud), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aid_robot_msgs__msg__FilterCloud));
  bool success = aid_robot_msgs__msg__FilterCloud__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aid_robot_msgs__msg__FilterCloud__destroy(aid_robot_msgs__msg__FilterCloud * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aid_robot_msgs__msg__FilterCloud__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aid_robot_msgs__msg__FilterCloud__Sequence__init(aid_robot_msgs__msg__FilterCloud__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__FilterCloud * data = NULL;

  if (size) {
    data = (aid_robot_msgs__msg__FilterCloud *)allocator.zero_allocate(size, sizeof(aid_robot_msgs__msg__FilterCloud), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aid_robot_msgs__msg__FilterCloud__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aid_robot_msgs__msg__FilterCloud__fini(&data[i - 1]);
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
aid_robot_msgs__msg__FilterCloud__Sequence__fini(aid_robot_msgs__msg__FilterCloud__Sequence * array)
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
      aid_robot_msgs__msg__FilterCloud__fini(&array->data[i]);
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

aid_robot_msgs__msg__FilterCloud__Sequence *
aid_robot_msgs__msg__FilterCloud__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aid_robot_msgs__msg__FilterCloud__Sequence * array = (aid_robot_msgs__msg__FilterCloud__Sequence *)allocator.allocate(sizeof(aid_robot_msgs__msg__FilterCloud__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aid_robot_msgs__msg__FilterCloud__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aid_robot_msgs__msg__FilterCloud__Sequence__destroy(aid_robot_msgs__msg__FilterCloud__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aid_robot_msgs__msg__FilterCloud__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aid_robot_msgs__msg__FilterCloud__Sequence__are_equal(const aid_robot_msgs__msg__FilterCloud__Sequence * lhs, const aid_robot_msgs__msg__FilterCloud__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aid_robot_msgs__msg__FilterCloud__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aid_robot_msgs__msg__FilterCloud__Sequence__copy(
  const aid_robot_msgs__msg__FilterCloud__Sequence * input,
  aid_robot_msgs__msg__FilterCloud__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aid_robot_msgs__msg__FilterCloud);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aid_robot_msgs__msg__FilterCloud * data =
      (aid_robot_msgs__msg__FilterCloud *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aid_robot_msgs__msg__FilterCloud__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aid_robot_msgs__msg__FilterCloud__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aid_robot_msgs__msg__FilterCloud__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
