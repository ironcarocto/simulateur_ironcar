import os

import io
from click.testing import CliRunner

from simulator.cli import init
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
