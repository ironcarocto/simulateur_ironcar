#include "colors.inc"

camera {
  ultra_wide_angle
  location <310, 10, 400>
  look_at  <320, 1, 200>
}
box {
  <0, 0, 0>,
  < 600, 600, 600>
  texture {
    uv_mapping
    pigment {
      image_map {
        jpeg "img_map_example.jpeg" once map_type 0
      }
    }
  }
}
light_source { <300, 300, 300> color White}
