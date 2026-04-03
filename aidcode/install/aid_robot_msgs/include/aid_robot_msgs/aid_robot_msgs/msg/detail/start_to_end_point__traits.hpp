// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:msg/StartToEndPoint.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__TRAITS_HPP_
#define AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/msg/detail/start_to_end_point__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'start'
// Member 'end'
#include "geometry_msgs/msg/detail/point32__traits.hpp"

namespace aid_robot_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const StartToEndPoint & msg,
  std::ostream & out)
{
  out << "{";
  // member: start
  {
    out << "start: ";
    to_flow_style_yaml(msg.start, out);
    out << ", ";
  }

  // member: end
  {
    out << "end: ";
    to_flow_style_yaml(msg.end, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const StartToEndPoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: start
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "start:\n";
    to_block_style_yaml(msg.start, out, indentation + 2);
  }

  // member: end
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "end:\n";
    to_block_style_yaml(msg.end, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const StartToEndPoint & msg, bool use_flow_style = false)
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
  const aid_robot_msgs::msg::StartToEndPoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::msg::StartToEndPoint & msg)
{
  return aid_robot_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::msg::StartToEndPoint>()
{
  return "aid_robot_msgs::msg::StartToEndPoint";
}

template<>
inline const char * name<aid_robot_msgs::msg::StartToEndPoint>()
{
  return "aid_robot_msgs/msg/StartToEndPoint";
}

template<>
struct has_fixed_size<aid_robot_msgs::msg::StartToEndPoint>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point32>::value> {};

template<>
struct has_bounded_size<aid_robot_msgs::msg::StartToEndPoint>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point32>::value> {};

template<>
struct is_message<aid_robot_msgs::msg::StartToEndPoint>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__MSG__DETAIL__START_TO_END_POINT__TRAITS_HPP_
