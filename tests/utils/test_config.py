import io
from unittest import mock

import toml

from kak_plugins.utils import config


@mock.patch.object(config, "open")
def test_read_calls_loader(mock_open):
    mock_open_context = mock.MagicMock()
    mock_open.return_value.__enter__.return_value = mock_open_context
    loader_spy = mock.MagicMock()
    config.read_config(loader_spy, "/home/kak_user/.config/plugins.toml")
    loader_spy.load.assert_called_once_with(mock_open_context)


@mock.patch.object(config, "open")
def test_read_can_parse_toml(mock_open):
    mock_open_context = io.StringIO(
        """
        [abc]
        a = "b"
        "git@github.com" = "https://github.com"
        """
    )
    mock_open.return_value.__enter__.return_value = mock_open_context
    result = config.read_config(toml, "filename doesn't matter")
    assert result == {"abc": {"a": "b", "git@github.com": "https://github.com"}}
