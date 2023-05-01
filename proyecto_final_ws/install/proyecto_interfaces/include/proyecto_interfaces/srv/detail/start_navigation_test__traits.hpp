// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from proyecto_interfaces:srv/StartNavigationTest.idl
// generated code does not contain a copyright notice

#ifndef PROYECTO_INTERFACES__SRV__DETAIL__START_NAVIGATION_TEST__TRAITS_HPP_
#define PROYECTO_INTERFACES__SRV__DETAIL__START_NAVIGATION_TEST__TRAITS_HPP_

#include "proyecto_interfaces/srv/detail/start_navigation_test__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<proyecto_interfaces::srv::StartNavigationTest_Request>()
{
  return "proyecto_interfaces::srv::StartNavigationTest_Request";
}

template<>
inline const char * name<proyecto_interfaces::srv::StartNavigationTest_Request>()
{
  return "proyecto_interfaces/srv/StartNavigationTest_Request";
}

template<>
struct has_fixed_size<proyecto_interfaces::srv::StartNavigationTest_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<proyecto_interfaces::srv::StartNavigationTest_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<proyecto_interfaces::srv::StartNavigationTest_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<proyecto_interfaces::srv::StartNavigationTest_Response>()
{
  return "proyecto_interfaces::srv::StartNavigationTest_Response";
}

template<>
inline const char * name<proyecto_interfaces::srv::StartNavigationTest_Response>()
{
  return "proyecto_interfaces/srv/StartNavigationTest_Response";
}

template<>
struct has_fixed_size<proyecto_interfaces::srv::StartNavigationTest_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<proyecto_interfaces::srv::StartNavigationTest_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<proyecto_interfaces::srv::StartNavigationTest_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<proyecto_interfaces::srv::StartNavigationTest>()
{
  return "proyecto_interfaces::srv::StartNavigationTest";
}

template<>
inline const char * name<proyecto_interfaces::srv::StartNavigationTest>()
{
  return "proyecto_interfaces/srv/StartNavigationTest";
}

template<>
struct has_fixed_size<proyecto_interfaces::srv::StartNavigationTest>
  : std::integral_constant<
    bool,
    has_fixed_size<proyecto_interfaces::srv::StartNavigationTest_Request>::value &&
    has_fixed_size<proyecto_interfaces::srv::StartNavigationTest_Response>::value
  >
{
};

template<>
struct has_bounded_size<proyecto_interfaces::srv::StartNavigationTest>
  : std::integral_constant<
    bool,
    has_bounded_size<proyecto_interfaces::srv::StartNavigationTest_Request>::value &&
    has_bounded_size<proyecto_interfaces::srv::StartNavigationTest_Response>::value
  >
{
};

template<>
struct is_service<proyecto_interfaces::srv::StartNavigationTest>
  : std::true_type
{
};

template<>
struct is_service_request<proyecto_interfaces::srv::StartNavigationTest_Request>
  : std::true_type
{
};

template<>
struct is_service_response<proyecto_interfaces::srv::StartNavigationTest_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PROYECTO_INTERFACES__SRV__DETAIL__START_NAVIGATION_TEST__TRAITS_HPP_
