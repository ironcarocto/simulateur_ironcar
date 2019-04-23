import os

from simulator import configuration
from simulator.pictures_generation import CONFIG_PATH, generate_profile_for_cadran
from tests.acceptances.fixtures import clone_template


def test_generate_profile_for_cadran_should_save_twice_as_many_images_as_configuration():
    with clone_template(template_name='simple_profil_generation') as path:
        # Given
        # initialise un dossier de travail - sinon le test declenche un FileNotFoundError sur getcwd
        os.chdir(path)
        output_path = path + '/photos'
        ground_path = path + '/grounds'
        conf = configuration.parse(CONFIG_PATH)
        conf['images_curve'] = 1

        # Where
        generate_profile_for_cadran(cadran_id=0,
                                    configuration=conf,
                                    ground_path=ground_path,
                                    photos_path=output_path)

        # Then
        image_number = count_png(output_path)
        assert image_number == conf['images_curve']


def count_png(photos_path_test):
    images_produced_by_povray = [x for x in os.listdir(photos_path_test) if x.endswith('.png')]
    image_number_init = len(images_produced_by_povray)
    return image_number_init
