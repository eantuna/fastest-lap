#include "gtest/gtest.h"
#include "lion/math/matrix_extensions.h"
#include "src/core/applications/optimal_laptime.h"
#include "src/core/vehicles/limebeer2014f1.h"
#include "lion/thirdparty/include/cppad/cppad.hpp"
#include "src/core/applications/steady_state.h"
#include "src/core/applications/circuit_preprocessor.h"

int main(int argc, char *argv[]) {
  std::string vehicle_path = "/opt/fastest-lap/database/vehicles/f1/limebeer-2014-f1.xml";
  if (argc > 1) {
    vehicle_path = argv[1];
    std::cout << "Vehicle path -> " << vehicle_path << std::endl;
  }

  Xml_document database = { vehicle_path, true };
  limebeer2014f1<CppAD::AD<scalar>>::cartesian car_cartesian = { database };

  std::string track_path = "/opt/fastest-lap/database/tracks/catalunya_2022/catalunya_2022.xml";
  if (argc > 2) {
    track_path = argv[2];
    std::cout << "Track path -> " << track_path << std::endl;
  }

  Xml_document catalunya_xml(track_path, true);
  Circuit_preprocessor catalunya_pproc(catalunya_xml);
  Track_by_polynomial catalunya(catalunya_pproc);

  limebeer2014f1<CppAD::AD<scalar>>::curvilinear<Track_by_polynomial>::Road_t road(catalunya);
  limebeer2014f1<CppAD::AD<scalar>>::curvilinear<Track_by_polynomial> car(database, road);

  // Start from the steady-state values at 50km/h-0g
  const scalar v = 50.0*KMH;
  auto ss = Steady_state(car_cartesian).solve(v,0.0,0.0);

  const auto& s = catalunya_pproc.s;
  const auto& n = s.size();

  // Construct control variables
  auto control_variables = Optimal_laptime<decltype(car)>::template Control_variables_type<>{};

  // steering wheel: optimize in the full mesh
  control_variables[decltype(car)::Chassis_type::front_axle_type::control_names::STEERING]
      = Optimal_laptime<decltype(car)>::create_full_mesh(std::vector<scalar>(n,ss.controls[decltype(car)::Chassis_type::front_axle_type::control_names::STEERING]), 50.0e0); 

  // throttle: optimize in the full mesh
  control_variables[decltype(car)::Chassis_type::control_names::throttle]
      = Optimal_laptime<decltype(car)>::create_full_mesh(std::vector<scalar>(n,ss.controls[decltype(car)::Chassis_type::control_names::throttle]), 20.0*8.0e-4); 

  // brake bias: don't optimize
  control_variables[decltype(car)::Chassis_type::control_names::brake_bias]
      = Optimal_laptime<decltype(car)>::create_dont_optimize(); 

  auto opts = Optimal_laptime<decltype(car)>::Options{};
  Optimal_laptime<decltype(car)> opt_laptime(s, true, true, car, {n,ss.inputs}, control_variables, opts);
  std::unique_ptr<Xml_document> doc = opt_laptime.xml();

  std::string output_path = "output.xml";
  if (argc > 3) {
    output_path = argv[3];
    std::cout << "Output path -> " << output_path << std::endl; 
  }
  bool saved = doc -> save(output_path);
}
