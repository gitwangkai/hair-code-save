// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aid_robot_msgs:srv/GetCurrentForbidden.idl
// generated code does not contain a copyright notice

#ifndef AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_FORBIDDEN__TRAITS_HPP_
#define AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_FORBIDDEN__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aid_robot_msgs/srv/detail/get_current_forbidden__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetCurrentForbidden_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetCurrentForbidden_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetCurrentForbidden_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace aid_robot_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aid_robot_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aid_robot_msgs::srv::GetCurrentForbidden_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::GetCurrentForbidden_Request & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::GetCurrentForbidden_Request>()
{
  return "aid_robot_msgs::srv::GetCurrentForbidden_Request";
}

template<>
inline const char * name<aid_robot_msgs::srv::GetCurrentForbidden_Request>()
{
  return "aid_robot_msgs/srv/GetCurrentForbidden_Request";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::GetCurrentForbidden_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::GetCurrentForbidden_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<aid_robot_msgs::srv::GetCurrentForbidden_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'message'
#include "aid_robot_msgs/msg/detail/start_to_end_point__traits.hpp"

namespace aid_robot_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetCurrentForbidden_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    if (msg.message.size() == 0) {
      out << "message: []";
    } else {
      out << "message: [";
      size_t pending_items = msg.message.size();
      for (auto item : msg.message) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetCurrentForbidden_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.message.size() == 0) {
      out << "message: []\n";
    } else {
      out << "message:\n";
      for (auto item : msg.message) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetCurrentForbidden_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace aid_robot_msgs

namespace rosidl_generator_traits
{

[[deprecated("use aid_robot_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aid_robot_msgs::srv::GetCurrentForbidden_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aid_robot_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aid_robot_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const aid_robot_msgs::srv::GetCurrentForbidden_Response & msg)
{
  return aid_robot_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aid_robot_msgs::srv::GetCurrentForbidden_Response>()
{
  return "aid_robot_msgs::srv::GetCurrentForbidden_Response";
}

template<>
inline const char * name<aid_robot_msgs::srv::GetCurrentForbidden_Response>()
{
  return "aid_robot_msgs/srv/GetCurrentForbidden_Response";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::GetCurrentForbidden_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aid_robot_msgs::srv::GetCurrentForbidden_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aid_robot_msgs::srv::GetCurrentForbidden_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aid_robot_msgs::srv::GetCurrentForbidden>()
{
  return "aid_robot_msgs::srv::GetCurrentForbidden";
}

template<>
inline const char * name<aid_robot_msgs::srv::GetCurrentForbidden>()
{
  return "aid_robot_msgs/srv/GetCurrentForbidden";
}

template<>
struct has_fixed_size<aid_robot_msgs::srv::GetCurrentForbidden>
  : std::integral_constant<
    bool,
    has_fixed_size<aid_robot_msgs::srv::GetCurrentForbidden_Request>::value &&
    has_fixed_size<aid_robot_msgs::srv::GetCurrentForbidden_Response>::value
  >
{
};

template<>
struct has_bounded_size<aid_robot_msgs::srv::GetCurrentForbidden>
  : std::integral_constant<
    bool,
    has_bounded_size<aid_robot_msgs::srv::GetCurrentForbidden_Request>::value &&
    has_bounded_size<aid_robot_msgs::srv::GetCurrentForbidden_Response>::value
  >
{
};

template<>
struct is_service<aid_robot_msgs::srv::GetCurrentForbidden>
  : std::true_type
{
};

template<>
struct is_service_request<aid_robot_msgs::srv::GetCurrentForbidden_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aid_robot_msgs::srv::GetCurrentForbidden_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AID_ROBOT_MSGS__SRV__DETAIL__GET_CURRENT_FORBIDDEN__TRAITS_HPP_
