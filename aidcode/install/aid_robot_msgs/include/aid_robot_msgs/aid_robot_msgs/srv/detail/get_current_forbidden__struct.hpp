// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aid_robot_msgs:srv/GetCurrentForbidden.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_FORBIDDEN__STRUCT_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_FORBIDDEN__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__srv__GetCurrentForbidden_Request __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__srv__GetCurrentForbidden_Request __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetCurrentForbidden_Request_
{
  using Type = GetCurrentForbidden_Request_<ContainerAllocator>;

  explicit GetCurrentForbidden_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit GetCurrentForbidden_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__srv__GetCurrentForbidden_Request
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__srv__GetCurrentForbidden_Request
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetCurrentForbidden_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetCurrentForbidden_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetCurrentForbidden_Request_

// alias to use template instance with default allocator
using GetCurrentForbidden_Request =
  aid_robot_msgs::srv::GetCurrentForbidden_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace aid_robot_msgs


// Include directives for member types
// Member 'message'
#include "aid_robot_msgs/msg/detail/start_to_end_point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__srv__GetCurrentForbidden_Response __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__srv__GetCurrentForbidden_Response __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetCurrentForbidden_Response_
{
  using Type = GetCurrentForbidden_Response_<ContainerAllocator>;

  explicit GetCurrentForbidden_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  explicit GetCurrentForbidden_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::vector<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator>>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::vector<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<aid_robot_msgs::msg::StartToEndPoint_<ContainerAllocator>>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__srv__GetCurrentForbidden_Response
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__srv__GetCurrentForbidden_Response
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentForbidden_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetCurrentForbidden_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetCurrentForbidden_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetCurrentForbidden_Response_

// alias to use template instance with default allocator
using GetCurrentForbidden_Response =
  aid_robot_msgs::srv::GetCurrentForbidden_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace aid_robot_msgs

namespace aid_robot_msgs
{

namespace srv
{

struct GetCurrentForbidden
{
  using Request = aid_robot_msgs::srv::GetCurrentForbidden_Request;
  using Response = aid_robot_msgs::srv::GetCurrentForbidden_Response;
};

}  // namespace srv

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_FORBIDDEN__STRUCT_HPP_
