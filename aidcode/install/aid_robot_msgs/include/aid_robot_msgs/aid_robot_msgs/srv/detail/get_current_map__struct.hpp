// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aid_robot_msgs:srv/GetCurrentMap.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_MAP__STRUCT_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_MAP__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__srv__GetCurrentMap_Request __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__srv__GetCurrentMap_Request __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetCurrentMap_Request_
{
  using Type = GetCurrentMap_Request_<ContainerAllocator>;

  explicit GetCurrentMap_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit GetCurrentMap_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__srv__GetCurrentMap_Request
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__srv__GetCurrentMap_Request
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentMap_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetCurrentMap_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetCurrentMap_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetCurrentMap_Request_

// alias to use template instance with default allocator
using GetCurrentMap_Request =
  aid_robot_msgs::srv::GetCurrentMap_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace aid_robot_msgs


#ifndef _WIN32
# define DEPRECATED__aid_robot_msgs__srv__GetCurrentMap_Response __attribute__((deprecated))
#else
# define DEPRECATED__aid_robot_msgs__srv__GetCurrentMap_Response __declspec(deprecated)
#endif

namespace aid_robot_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetCurrentMap_Response_
{
  using Type = GetCurrentMap_Response_<ContainerAllocator>;

  explicit GetCurrentMap_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->map_id = 0ul;
      this->map_file = "";
      this->map_name = "";
    }
  }

  explicit GetCurrentMap_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : map_file(_alloc),
    map_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->map_id = 0ul;
      this->map_file = "";
      this->map_name = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _map_id_type =
    uint32_t;
  _map_id_type map_id;
  using _map_file_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _map_file_type map_file;
  using _map_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _map_name_type map_name;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__map_id(
    const uint32_t & _arg)
  {
    this->map_id = _arg;
    return *this;
  }
  Type & set__map_file(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->map_file = _arg;
    return *this;
  }
  Type & set__map_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->map_name = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aid_robot_msgs__srv__GetCurrentMap_Response
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aid_robot_msgs__srv__GetCurrentMap_Response
    std::shared_ptr<aid_robot_msgs::srv::GetCurrentMap_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetCurrentMap_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->map_id != other.map_id) {
      return false;
    }
    if (this->map_file != other.map_file) {
      return false;
    }
    if (this->map_name != other.map_name) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetCurrentMap_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetCurrentMap_Response_

// alias to use template instance with default allocator
using GetCurrentMap_Response =
  aid_robot_msgs::srv::GetCurrentMap_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace aid_robot_msgs

namespace aid_robot_msgs
{

namespace srv
{

struct GetCurrentMap
{
  using Request = aid_robot_msgs::srv::GetCurrentMap_Request;
  using Response = aid_robot_msgs::srv::GetCurrentMap_Response;
};

}  // namespace srv

}  // namespace aid_robot_msgs

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_MAP__STRUCT_HPP_
