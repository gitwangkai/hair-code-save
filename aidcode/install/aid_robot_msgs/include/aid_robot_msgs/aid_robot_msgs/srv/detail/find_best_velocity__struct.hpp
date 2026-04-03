// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aid_robot_msgs:srv/FindBestVelocity.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__STRUCT_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__STRUCT_HPP_

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
# define DEPRECATED__aid_robot_msgs__srv__FindBestVelocity_Request __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__srv__FindBestVelocity_Request __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct FindBestVelocity_Request_
{
  using Type = FindBestVelocity_Request_<ContainerAllocator>;

  explicit FindBestVelocity_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->max_angular_velocity = 0.0f;
      this->max_speed = 0.0f;
      this->len = 0.0f;
    }
  }

  explicit FindBestVelocity_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->max_angular_velocity = 0.0f;
      this->max_speed = 0.0f;
      this->len = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _max_angular_velocity_type =
    float;
  _max_angular_velocity_type max_angular_velocity;
  using _max_speed_type =
    float;
  _max_speed_type max_speed;
  using _len_type =
    float;
  _len_type len;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__max_angular_velocity(
    const float & _arg)
  {
    this->max_angular_velocity = _arg;
    return *this;
  }
  Type & set__max_speed(
    const float & _arg)
  {
    this->max_speed = _arg;
    return *this;
  }
  Type & set__len(
    const float & _arg)
  {
    this->len = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__srv__FindBestVelocity_Request
    std::shared_ptr<aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__srv__FindBestVelocity_Request
    std::shared_ptr<aid_robot_msgs::srv::FindBestVelocity_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FindBestVelocity_Request_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->max_angular_velocity != other.max_angular_velocity) {
      return false;
    }
    if (this->max_speed != other.max_speed) {
      return false;
    }
    if (this->len != other.len) {
      return false;
    }
    return true;
  }
  bool operator!=(const FindBestVelocity_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FindBestVelocity_Request_

// alias to use template instance with default allocator
using FindBestVelocity_Request =
  aid_robot_msgs::srv::FindBestVelocity_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace aid_robot_msgs


// Include directives for member types
// Member 'cmd_vel'
#include "geometry_msgs/msg/detail/twist__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__srv__FindBestVelocity_Response __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__srv__FindBestVelocity_Response __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct FindBestVelocity_Response_
{
  using Type = FindBestVelocity_Response_<ContainerAllocator>;

  explicit FindBestVelocity_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : cmd_vel(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->msg = "";
    }
  }

  explicit FindBestVelocity_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : cmd_vel(_alloc, _init),
    msg(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->msg = "";
    }
  }

  // field types and members
  using _cmd_vel_type =
    geometry_msgs::msg::Twist_<ContainerAllocator>;
  _cmd_vel_type cmd_vel;
  using _success_type =
    bool;
  _success_type success;
  using _msg_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _msg_type msg;

  // setters for named parameter idiom
  Type & set__cmd_vel(
    const geometry_msgs::msg::Twist_<ContainerAllocator> & _arg)
  {
    this->cmd_vel = _arg;
    return *this;
  }
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__msg(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->msg = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__srv__FindBestVelocity_Response
    std::shared_ptr<aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__srv__FindBestVelocity_Response
    std::shared_ptr<aid_robot_msgs::srv::FindBestVelocity_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FindBestVelocity_Response_ & other) const
  {
    if (this->cmd_vel != other.cmd_vel) {
      return false;
    }
    if (this->success != other.success) {
      return false;
    }
    if (this->msg != other.msg) {
      return false;
    }
    return true;
  }
  bool operator!=(const FindBestVelocity_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FindBestVelocity_Response_

// alias to use template instance with default allocator
using FindBestVelocity_Response =
  aid_robot_msgs::srv::FindBestVelocity_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace aid_robot_msgs

namespace aid_robot_msgs
{

namespace srv
{

struct FindBestVelocity
{
  using Request = aid_robot_msgs::srv::FindBestVelocity_Request;
  using Response = aid_robot_msgs::srv::FindBestVelocity_Response;
};

}  // namespace srv

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__FIND_BEST_VELOCITY__STRUCT_HPP_
