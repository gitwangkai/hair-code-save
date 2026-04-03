// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aid_robot_msgs:msg/Rectangle.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__RECTANGLE__STRUCT_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__RECTANGLE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'center_point'
#include "geometry_msgs/msg/detail/point32__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__msg__Rectangle __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__msg__Rectangle __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Rectangle_
{
  using Type = Rectangle_<ContainerAllocator>;

  explicit Rectangle_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : center_point(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->side_length = 0.0f;
      this->grayscale = 0;
    }
  }

  explicit Rectangle_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : center_point(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->side_length = 0.0f;
      this->grayscale = 0;
    }
  }

  // field types and members
  using _center_point_type =
    geometry_msgs::msg::Point32_<ContainerAllocator>;
  _center_point_type center_point;
  using _side_length_type =
    float;
  _side_length_type side_length;
  using _grayscale_type =
    uint8_t;
  _grayscale_type grayscale;

  // setters for named parameter idiom
  Type & set__center_point(
    const geometry_msgs::msg::Point32_<ContainerAllocator> & _arg)
  {
    this->center_point = _arg;
    return *this;
  }
  Type & set__side_length(
    const float & _arg)
  {
    this->side_length = _arg;
    return *this;
  }
  Type & set__grayscale(
    const uint8_t & _arg)
  {
    this->grayscale = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::msg::Rectangle_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::msg::Rectangle_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::msg::Rectangle_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::msg::Rectangle_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::msg::Rectangle_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::msg::Rectangle_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::msg::Rectangle_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::msg::Rectangle_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::msg::Rectangle_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::msg::Rectangle_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__msg__Rectangle
    std::shared_ptr<aid_robot_msgs::msg::Rectangle_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__msg__Rectangle
    std::shared_ptr<aid_robot_msgs::msg::Rectangle_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Rectangle_ & other) const
  {
    if (this->center_point != other.center_point) {
      return false;
    }
    if (this->side_length != other.side_length) {
      return false;
    }
    if (this->grayscale != other.grayscale) {
      return false;
    }
    return true;
  }
  bool operator!=(const Rectangle_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Rectangle_

// alias to use template instance with default allocator
using Rectangle =
  aid_robot_msgs::msg::Rectangle_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__RECTANGLE__STRUCT_HPP_
