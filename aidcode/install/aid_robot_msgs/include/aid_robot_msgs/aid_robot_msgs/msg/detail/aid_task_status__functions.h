// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from aid_robot_msgs:msg/AidTaskStatus.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__FUNCTIONS_H_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "aid_robot_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "aid_robot_msgs/msg/detail/aid_task_status__struct.h"

/// Initialize msg/AidTaskStatus message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * aid_robot_msgs__msg__AidTaskStatus
 * )) before or use
 * aid_robot_msgs__msg__AidTaskStatus__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
bool
aid_robot_msgs__msg__AidTaskStatus__init(aid_robot_msgs__msg__AidTaskStatus * msg);

/// Finalize msg/AidTaskStatus message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
void
aid_robot_msgs__msg__AidTaskStatus__fini(aid_robot_msgs__msg__AidTaskStatus * msg);

/// Create msg/AidTaskStatus message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * aid_robot_msgs__msg__AidTaskStatus__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
aid_robot_msgs__msg__AidTaskStatus *
aid_robot_msgs__msg__AidTaskStatus__create();

/// Destroy msg/AidTaskStatus message.
/**
 * It calls
 * aid_robot_msgs__msg__AidTaskStatus__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
void
aid_robot_msgs__msg__AidTaskStatus__destroy(aid_robot_msgs__msg__AidTaskStatus * msg);

/// Check for msg/AidTaskStatus message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
bool
aid_robot_msgs__msg__AidTaskStatus__are_equal(const aid_robot_msgs__msg__AidTaskStatus * lhs, const aid_robot_msgs__msg__AidTaskStatus * rhs);

/// Copy a msg/AidTaskStatus message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
bool
aid_robot_msgs__msg__AidTaskStatus__copy(
  const aid_robot_msgs__msg__AidTaskStatus * input,
  aid_robot_msgs__msg__AidTaskStatus * output);

/// Initialize array of msg/AidTaskStatus messages.
/**
 * It allocates the memory for the number of elements and calls
 * aid_robot_msgs__msg__AidTaskStatus__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
bool
aid_robot_msgs__msg__AidTaskStatus__Sequence__init(aid_robot_msgs__msg__AidTaskStatus__Sequence * array, size_t size);

/// Finalize array of msg/AidTaskStatus messages.
/**
 * It calls
 * aid_robot_msgs__msg__AidTaskStatus__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
void
aid_robot_msgs__msg__AidTaskStatus__Sequence__fini(aid_robot_msgs__msg__AidTaskStatus__Sequence * array);

/// Create array of msg/AidTaskStatus messages.
/**
 * It allocates the memory for the array and calls
 * aid_robot_msgs__msg__AidTaskStatus__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
aid_robot_msgs__msg__AidTaskStatus__Sequence *
aid_robot_msgs__msg__AidTaskStatus__Sequence__create(size_t size);

/// Destroy array of msg/AidTaskStatus messages.
/**
 * It calls
 * aid_robot_msgs__msg__AidTaskStatus__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
void
aid_robot_msgs__msg__AidTaskStatus__Sequence__destroy(aid_robot_msgs__msg__AidTaskStatus__Sequence * array);

/// Check for msg/AidTaskStatus message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
bool
aid_robot_msgs__msg__AidTaskStatus__Sequence__are_equal(const aid_robot_msgs__msg__AidTaskStatus__Sequence * lhs, const aid_robot_msgs__msg__AidTaskStatus__Sequence * rhs);

/// Copy an array of msg/AidTaskStatus messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_aid_robot_msgs
bool
aid_robot_msgs__msg__AidTaskStatus__Sequence__copy(
  const aid_robot_msgs__msg__AidTaskStatus__Sequence * input,
  aid_robot_msgs__msg__AidTaskStatus__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__FUNCTIONS_H_
