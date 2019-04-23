# Configuration.json

le fichier de configuration par défaut est dans [simulator/profil_generation_template/configuration.json](../simulator/profil_generation_template/configuration.json)

```json
{
    "version": "2019/02/23",
    "dataset_id": "dataset",
    "line_width_cm": 6,
    "line_spread_cm" : 40,
    "dash_length_cm" : 40,
    "conversion_pixel_to_cm" : 0.3,
    "image_width" : 1000,
    "image_height": 1000,
    "command_distance_cm" : 20,
    "origin_pool_start":100,
    "origin_pool_end":500,
    "origin_pool_step":5,

    "end_pool_top_start":600,
    "end_pool_top_end":1000,
    "end_pool_top_step":5,

    "end_pool_right_start":10,
    "end_pool_right_end":900,
    "end_pool_right_step":5,

    "radius_pool_start":600,
    "radius_pool_end":3000,
    "radius_pool_step":100,

    "road_median_line_color":"#66ec04",
    "road_outer_line_color": "#ffffff",

    "images_curve":2
}
```

### road_median_line_color

Couleur de la ligne centrale.

* valeur par défaut : ``#66ec04``.

![Banner](docs/images/21_cmd_0.png)

Seule [les couleurs web sous forme de code hexadécimale](https://www.w3.org/TR/REC-html40/types.html#h-6.5) sont supportées.

### road_outer_line_color

Couleur du marquage extérieure.

* valeur par défaut : ``#ffffff``.

![Banner](docs/images/21_cmd_0.png)

Seule [les couleurs web sous forme de code hexadécimale](https://www.w3.org/TR/REC-html40/types.html#h-6.5) sont supportées.

### images_curve

Nombre d'images générées par terrains (grounds)

* option obligatoire
* valeur par défaut : 2
