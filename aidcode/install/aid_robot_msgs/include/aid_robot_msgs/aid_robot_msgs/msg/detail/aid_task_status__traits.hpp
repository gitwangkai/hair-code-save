// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:msg/AidTaskStatus.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__TRAITS_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/msg/detail/aid_task_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aid_robot_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const AidTaskStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: task_type
  {
    out << "task_type: ";
    rosidl_generator_traits::value_to_yaml(msg.task_type, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AidTaskStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: task_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "task_type: ";
    rosidl_generator_traits::value_to_yaml(msg.task_type, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AidTaskStatus & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace aid_robot_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aid_robot_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aid_robot_msgs::msg::AidTaskStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::msg::AidTaskStatus & msg)
{
  return aid_robot_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::msg::AidTaskStatus>()
{
  return "aid_robot_msgs::msg::AidTaskStatus";
}

template<>
inline const char * name<aid_robot_msgs::msg::AidTaskStatus>()
{
  return "aid_robot_msgs/msg/AidTaskStatus";
}

template<>
struct has_fixed_size<aid_robot_msgs::msg::AidTaskStatus>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<aid_robot_msgs::msg::AidTaskStatus>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<aid_robot_msgs::msg::AidTaskStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__AID_TASK_STATUS__TRAITS_HPP_
