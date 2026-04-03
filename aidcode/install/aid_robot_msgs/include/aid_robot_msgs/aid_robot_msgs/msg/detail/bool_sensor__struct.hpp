// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aid_robot_msgs:msg/BoolSensor.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__BOOL_SENSOR__STRUCT_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__BOOL_SENSOR__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__msg__BoolSensor __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__msg__BoolSensor __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct BoolSensor_
{
  using Type = BoolSensor_<ContainerAllocator>;

  explicit BoolSensor_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->triggered = false;
    }
  }

  explicit BoolSensor_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->triggered = false;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _triggered_type =
    bool;
  _triggered_type triggered;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__triggered(
    const bool & _arg)
  {
    this->triggered = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::msg::BoolSensor_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::msg::BoolSensor_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::msg::BoolSensor_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::msg::BoolSensor_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::msg::BoolSensor_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::msg::BoolSensor_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::msg::BoolSensor_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::msg::BoolSensor_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::msg::BoolSensor_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::msg::BoolSensor_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__msg__BoolSensor
    std::shared_ptr<aid_robot_msgs::msg::BoolSensor_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__msg__BoolSensor
    std::shared_ptr<aid_robot_msgs::msg::BoolSensor_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const BoolSensor_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->triggered != other.triggered) {
      return false;
    }
    return true;
  }
  bool operator!=(const BoolSensor_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct BoolSensor_

// alias to use template instance with default allocator
using BoolSensor =
  aid_robot_msgs::msg::BoolSensor_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__BOOL_SENSOR__STRUCT_HPP_
