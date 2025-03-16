#include "src/core/applications/circuit_preprocessor.h"

int main(int argc, char *argv[]) {
  //std::string track_left_kml = "/opt/fastest-lap/database/tracks/catalunya_ea/catalunya_2022_left_ea.kml";
  //std::string track_right_kml = "/opt/fastest-lap/database/tracks/catalunya_ea/catalunya_2022_right_ea.kml";
  std::string track_left_kml = "/opt/fastest-lap/database/tracks/mia/mia-international-edge-1-output2-left.kml";
  std::string track_right_kml = "/opt/fastest-lap/database/tracks/mia/mia-international-edge-0-output2-right.kml";

  Xml_document coord_left_kml(track_left_kml, true);
  Xml_document coord_right_kml(track_right_kml, true);

  Circuit_preprocessor::Options options;

  options.with_elevation = false;
  // options.eps_k = 3.0e4;
  // options.eps_n = 1.0e-2;
  // options.eps_c = 1.0e-2;
  // options.eps_d = 1.0e-2;
  // options.maximum_yaw_dot = 1.0;
  // options.maximum_dyaw_dot = 1.0;
  //options.print_level = 7;

  Circuit_preprocessor circuit(coord_left_kml, coord_right_kml, options, 700);

  std::unique_ptr<Xml_document> doc = circuit.xml();
  
  bool saved = doc -> save("circuit-output.xml");
}