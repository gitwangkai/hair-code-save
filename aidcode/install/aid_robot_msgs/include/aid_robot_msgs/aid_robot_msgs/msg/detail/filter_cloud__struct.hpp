// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aid_robot_msgs:msg/FilterCloud.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__FILTER_CLOUD__STRUCT_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__FILTER_CLOUD__STRUCT_HPP_

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
// Member 'filtered_points'
// Member 'raw_points'
#include "sensor_msgs/msg/detail/point_cloud2__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__msg__FilterCloud __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__msg__FilterCloud __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct FilterCloud_
{
  using Type = FilterCloud_<ContainerAllocator>;

  explicit FilterCloud_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    filtered_points(_init),
    raw_points(_init)
  {
    (void)_init;
  }

  explicit FilterCloud_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    filtered_points(_alloc, _init),
    raw_points(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _filtered_points_type =
    sensor_msgs::msg::PointCloud2_<ContainerAllocator>;
  _filtered_points_type filtered_points;
  using _raw_points_type =
    sensor_msgs::msg::PointCloud2_<ContainerAllocator>;
  _raw_points_type raw_points;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__filtered_points(
    const sensor_msgs::msg::PointCloud2_<ContainerAllocator> & _arg)
  {
    this->filtered_points = _arg;
    return *this;
  }
  Type & set__raw_points(
    const sensor_msgs::msg::PointCloud2_<ContainerAllocator> & _arg)
  {
    this->raw_points = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::msg::FilterCloud_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::msg::FilterCloud_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::msg::FilterCloud_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::msg::FilterCloud_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::msg::FilterCloud_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::msg::FilterCloud_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::msg::FilterCloud_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::msg::FilterCloud_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::msg::FilterCloud_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::msg::FilterCloud_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__msg__FilterCloud
    std::shared_ptr<aid_robot_msgs::msg::FilterCloud_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__msg__FilterCloud
    std::shared_ptr<aid_robot_msgs::msg::FilterCloud_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FilterCloud_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->filtered_points != other.filtered_points) {
      return false;
    }
    if (this->raw_points != other.raw_points) {
      return false;
    }
    return true;
  }
  bool operator!=(const FilterCloud_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FilterCloud_

// alias to use template instance with default allocator
using FilterCloud =
  aid_robot_msgs::msg::FilterCloud_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__FILTER_CLOUD__STRUCT_HPP_
