import os

import io
from click.testing import CliRunner

from simulator.cli import init, generate
from tests.acceptances.fixtures import clone_template


def test_cli_init_should_generate_profile_in_working_directory():
    with clone_template(template_name='empty_working_directory') as cwd:
        # Given
        os.chdir(cwd)

        # Where
        runner = CliRunner()
        result = runner.invoke(init)

        # Then
        assert result.exit_code == 0
        assert os.path.isfile(os.path.join(cwd, 'configuration.json'))

def test_cli_init_should_not_erase_existing_configuration():
    with clone_template(template_name='simple_profil_generation') as cwd:
        # Given
        os.chdir(cwd)
        original_configuration_content = io.open(os.path.join(cwd, 'configuration.json'), 'r').read()

        # Where
        runner = CliRunner()
        result = runner.invoke(init)

        # Then
        assert result.exit_code == 1
        assert original_configuration_content == io.open(os.path.join(cwd, 'configuration.json'), 'r').read()


def test_cli_generate_should_generate_one_photo_by_cadran():
    with clone_template(template_name='simple_profil_generation') as cwd:
        # Given
        os.remove(os.path.join(cwd, 'photos', '.gitkeep'))
        os.chdir(cwd)

        # Where
        runner = CliRunner()
        result = runner.invoke(generate)

        # Then
        photos_path = os.path.join(cwd, 'photos')
        images_produced_by_povray = [x for x in os.listdir(photos_path)]
        assert result.exit_code == 0
        assert len(images_produced_by_povray) == 5
