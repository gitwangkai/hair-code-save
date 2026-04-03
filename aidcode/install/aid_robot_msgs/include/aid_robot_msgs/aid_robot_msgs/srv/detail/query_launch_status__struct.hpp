// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aid_robot_msgs:srv/QueryLaunchStatus.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__QUERY_LAUNCH_STATUS__STRUCT_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__QUERY_LAUNCH_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__srv__QueryLaunchStatus_Request __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__srv__QueryLaunchStatus_Request __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct QueryLaunchStatus_Request_
{
  using Type = QueryLaunchStatus_Request_<ContainerAllocator>;

  explicit QueryLaunchStatus_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->launch_file = "";
    }
  }

  explicit QueryLaunchStatus_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : launch_file(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->launch_file = "";
    }
  }

  // field types and members
  using _launch_file_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _launch_file_type launch_file;

  // setters for named parameter idiom
  Type & set__launch_file(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->launch_file = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__srv__QueryLaunchStatus_Request
    std::shared_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__srv__QueryLaunchStatus_Request
    std::shared_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const QueryLaunchStatus_Request_ & other) const
  {
    if (this->launch_file != other.launch_file) {
      return false;
    }
    return true;
  }
  bool operator!=(const QueryLaunchStatus_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct QueryLaunchStatus_Request_

// alias to use template instance with default allocator
using QueryLaunchStatus_Request =
  aid_robot_msgs::srv::QueryLaunchStatus_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace aid_robot_msgs


#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__srv__QueryLaunchStatus_Response __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__srv__QueryLaunchStatus_Response __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct QueryLaunchStatus_Response_
{
  using Type = QueryLaunchStatus_Response_<ContainerAllocator>;

  explicit QueryLaunchStatus_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit QueryLaunchStatus_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__srv__QueryLaunchStatus_Response
    std::shared_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__srv__QueryLaunchStatus_Response
    std::shared_ptr<aid_robot_msgs::srv::QueryLaunchStatus_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const QueryLaunchStatus_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const QueryLaunchStatus_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct QueryLaunchStatus_Response_

// alias to use template instance with default allocator
using QueryLaunchStatus_Response =
  aid_robot_msgs::srv::QueryLaunchStatus_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace aid_robot_msgs

namespace aid_robot_msgs
{

namespace srv
{

struct QueryLaunchStatus
{
  using Request = aid_robot_msgs::srv::QueryLaunchStatus_Request;
  using Response = aid_robot_msgs::srv::QueryLaunchStatus_Response;
};

}  // namespace srv

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__QUERY_LAUNCH_STATUS__STRUCT_HPP_
