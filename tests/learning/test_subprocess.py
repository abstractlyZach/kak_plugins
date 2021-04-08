import subprocess

import pytest

pytestmark = pytest.mark.os("these tests interact with the OS")


def test_exit_1_yields_return_code_0():
    result = subprocess.run(["exit", "1"], shell=True, check=True)
    assert result.returncode == 0


def test_cant_find_exit_without_shell():
    with pytest.raises(FileNotFoundError):
        subprocess.run(["exit", "1"], check=True)


def test_exit_string_without_shell():
    with pytest.raises(FileNotFoundError):
        subprocess.run("exit 1")


def test_catch_error():
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run("exit 1", shell=True, check=True)


def test_error_without_checking():
    result = subprocess.run("exit 1", shell=True)
    assert result.returncode == 1


# ok, it seems like I should just always use shell=True???


def test_echo_output():
    result = subprocess.run('echo "hi there"', shell=True, capture_output=True)
    # decode because it's a byte string
    result_string = str(result.stdout, encoding="utf-8")
    # strip off the newline
    assert result_string.strip() == "hi there"


def test_multiline_output():
    result = subprocess.run(
        'echo "hi there\nhow are you?"', shell=True, capture_output=True
    )
    result_string = str(result.stdout, encoding="utf-8")
    assert result_string.strip().split("\n") == ["hi there", "how are you?"]


# guess I don't actually need shell=True...


def test_write_to_clipboard():
    subprocess.run("wl-copy", input="writing to the clipboard", text=True)


def test_read_from_kcr():
    result = subprocess.run(
        ["kcr", "get", "--value", "buffile"], capture_output=True, check=True
    )
    output = str(result.stdout, "utf-8").strip()
    assert (
        output
        == '["/home/zach/workspace/kak_plugins/tests/learning/test_subprocess.py"]'
    )
