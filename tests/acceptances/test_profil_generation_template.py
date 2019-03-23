import json
import os

import io
from click.testing import CliRunner
from simulator.cli import init

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFIL_GENERATION_TEMPLATE_DIR = os.path.join(ROOT_DIR, '..', '..', 'simulator', 'profil_generation_template')

def test_configuration_json_should_have_a_version_attribute():
    # Given

    # When
    with io.open(os.path.join(PROFIL_GENERATION_TEMPLATE_DIR, 'configuration.json')) as fp:
        configuration = json.load(fp)

    # Then
    assert "version" in configuration

def test_grounds_directory_should_contain_at_least_one_ground():
    # Given
    ground_path = os.path.join(PROFIL_GENERATION_TEMPLATE_DIR, 'grounds')

    # When
    ground_files = [f for f in os.listdir(ground_path) if os.path.isfile(os.path.join(ground_path, f))]

    # Then
    assert len(ground_files) >= 1

def test_photos_directory_should_be_empty():
    # Given
    photos_path = os.path.join(PROFIL_GENERATION_TEMPLATE_DIR, 'photos')

    # When
    photos_files = [f for f in os.listdir(photos_path) if os.path.isfile(os.path.join(photos_path, f))]

    # Then
    assert '.gitkeep' in photos_files
    assert len(photos_files) == 1
