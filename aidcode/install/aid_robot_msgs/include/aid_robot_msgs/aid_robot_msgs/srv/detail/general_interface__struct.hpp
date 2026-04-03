// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aid_robot_msgs:srv/GeneralInterface.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__GENERAL_INTERFACE__STRUCT_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__GENERAL_INTERFACE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__srv__GeneralInterface_Request __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__srv__GeneralInterface_Request __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GeneralInterface_Request_
{
  using Type = GeneralInterface_Request_<ContainerAllocator>;

  explicit GeneralInterface_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->body = "";
    }
  }

  explicit GeneralInterface_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : body(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->body = "";
    }
  }

  // field types and members
  using _body_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _body_type body;

  // setters for named parameter idiom
  Type & set__body(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->body = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__srv__GeneralInterface_Request
    std::shared_ptr<aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__srv__GeneralInterface_Request
    std::shared_ptr<aid_robot_msgs::srv::GeneralInterface_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GeneralInterface_Request_ & other) const
  {
    if (this->body != other.body) {
      return false;
    }
    return true;
  }
  bool operator!=(const GeneralInterface_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GeneralInterface_Request_

// alias to use template instance with default allocator
using GeneralInterface_Request =
  aid_robot_msgs::srv::GeneralInterface_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace aid_robot_msgs


#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__srv__GeneralInterface_Response __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__srv__GeneralInterface_Response __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GeneralInterface_Response_
{
  using Type = GeneralInterface_Response_<ContainerAllocator>;

  explicit GeneralInterface_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->result = "";
    }
  }

  explicit GeneralInterface_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->result = "";
    }
  }

  // field types and members
  using _result_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__result(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__srv__GeneralInterface_Response
    std::shared_ptr<aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__srv__GeneralInterface_Response
    std::shared_ptr<aid_robot_msgs::srv::GeneralInterface_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GeneralInterface_Response_ & other) const
  {
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const GeneralInterface_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GeneralInterface_Response_

// alias to use template instance with default allocator
using GeneralInterface_Response =
  aid_robot_msgs::srv::GeneralInterface_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace aid_robot_msgs

namespace aid_robot_msgs
{

namespace srv
{

struct GeneralInterface
{
  using Request = aid_robot_msgs::srv::GeneralInterface_Request;
  using Response = aid_robot_msgs::srv::GeneralInterface_Response;
};

}  // namespace srv

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__GENERAL_INTERFACE__STRUCT_HPP_
