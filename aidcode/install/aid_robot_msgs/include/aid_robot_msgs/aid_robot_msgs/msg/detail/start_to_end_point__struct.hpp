// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aid_robot_msgs:msg/StartToEndPoint.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__STRUCT_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'start'
// Member 'end'
#include "geometry_msgs/msg/detail/point32__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__msg__StartToEndPoint __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__msg__StartToEndPoint __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct StartToEndPoint_
{
  using Type = StartToEndPoint_<ContainerAllocator>;

  explicit StartToEndPoint_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : start(_init),
    end(_init)
  {
    (void)_init;
  }

  explicit StartToEndPoint_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : start(_alloc, _init),
    end(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _start_type =
    geometry_msgs::msg::Point32_<ContainerAllocator>;
  _start_type start;
  using _end_type =
    geometry_msgs::msg::Point32_<ContainerAllocator>;
  _end_type end;

  // setters for named parameter idiom
  Type & set__start(
    const geometry_msgs::msg::Point32_<ContainerAllocator> & _arg)
  {
    this->start = _arg;
    return *this;
  }
  Type & set__end(
    const geometry_msgs::msg::Point32_<ContainerAllocator> & _arg)
  {
    this->end = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__msg__StartToEndPoint
    std::shared_ptr<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__msg__StartToEndPoint
    std::shared_ptr<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const StartToEndPoint_ & other) const
  {
    if (this->start != other.start) {
      return false;
    }
    if (this->end != other.end) {
      return false;
    }
    return true;
  }
  bool operator!=(const StartToEndPoint_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct StartToEndPoint_

// alias to use template instance with default allocator
using StartToEndPoint =
  aid_robot_msgs::msg::StartToEndPoint_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__STRUCT_HPP_
