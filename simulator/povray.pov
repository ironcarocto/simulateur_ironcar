#version 3.7;
#include "colors.inc"

global_settings { assumed_gamma 1.0 }

camera {
  ultra_wide_angle
  location <500, 60, 0>
  look_at  <500, 50, 100>
}
box {
  <0, 0, 0>,
  < 1000, 1000, 1000>
  // http://www.f-lohmueller.de/pov_tut/backgrnd/p_sky9.htm
  texture {
    uv_mapping
    pigment {
      image_map {
        jpeg "test.jpg" once map_type 0
      }
    }
  }
}
light_source { <500, 500, 500> color White}
