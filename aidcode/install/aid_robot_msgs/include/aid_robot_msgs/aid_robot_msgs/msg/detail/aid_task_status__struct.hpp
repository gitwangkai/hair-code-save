// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aid_robot_msgs:msg/AidTaskStatus.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__STRUCT_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__msg__AidTaskStatus __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__msg__AidTaskStatus __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct AidTaskStatus_
{
  using Type = AidTaskStatus_<ContainerAllocator>;

  explicit AidTaskStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0l;
      this->task_type = 0l;
    }
  }

  explicit AidTaskStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0l;
      this->task_type = 0l;
    }
  }

  // field types and members
  using _status_type =
    int32_t;
  _status_type status;
  using _task_type_type =
    int32_t;
  _task_type_type task_type;

  // setters for named parameter idiom
  Type & set__status(
    const int32_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__task_type(
    const int32_t & _arg)
  {
    this->task_type = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__msg__AidTaskStatus
    std::shared_ptr<aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__msg__AidTaskStatus
    std::shared_ptr<aid_robot_msgs::msg::AidTaskStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AidTaskStatus_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->task_type != other.task_type) {
      return false;
    }
    return true;
  }
  bool operator!=(const AidTaskStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AidTaskStatus_

// alias to use template instance with default allocator
using AidTaskStatus =
  aid_robot_msgs::msg::AidTaskStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__STRUCT_HPP_
