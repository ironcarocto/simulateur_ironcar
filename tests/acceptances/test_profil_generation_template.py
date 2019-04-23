import os

from simulator import configuration

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFIL_GENERATION_TEMPLATE_DIR = os.path.join(ROOT_DIR, '..', '..', 'simulator', 'profil_generation_template')


def test_check_default_configuration_is_valid():
    # Given

    # When
    conf = configuration.parse(os.path.join(PROFIL_GENERATION_TEMPLATE_DIR, 'configuration.json'))

    # Then
    assert "version" in conf


def test_check_grounds_directory_contains_at_least_one_ground():
    # Given
    ground_path = os.path.join(PROFIL_GENERATION_TEMPLATE_DIR, 'grounds')

    # When
    ground_files = [f for f in os.listdir(ground_path) if os.path.isfile(os.path.join(ground_path, f))]

    # Then
    assert len(ground_files) >= 1


def test_check_photos_directory_is_empty():
    # Given
    photos_path = os.path.join(PROFIL_GENERATION_TEMPLATE_DIR, 'photos')

    # When
    photos_files = [f for f in os.listdir(photos_path) if os.path.isfile(os.path.join(photos_path, f))]

    # Then
    assert '.gitkeep' in photos_files
    assert len(photos_files) == 1
