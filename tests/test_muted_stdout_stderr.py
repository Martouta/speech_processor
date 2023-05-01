import sys
from app.muted_stdout_stderr import muted_stdout_stderr


class TestMutedStdoutStderr:
    def test_muting_stdout(self, capfd):
        print("This should be captured")
        with muted_stdout_stderr():
            print("This should NOT be captured")
        print("This should be captured again")

        captured = capfd.readouterr()
        assert captured.out == "This should be captured\nThis should be captured again\n"

    def test_muting_stderr(self, capfd):
        sys.stderr.write("This should be captured\n")
        with muted_stdout_stderr():
            sys.stderr.write("This should NOT be captured\n")
        sys.stderr.write("This should be captured again\n")

        captured = capfd.readouterr()
        assert captured.err == "This should be captured\nThis should be captured again\n"

    def test_muting_both_stdout_and_stderr(self, capfd):
        print("stdout: This should be captured")
        sys.stderr.write("stderr: This should be captured\n")
        with muted_stdout_stderr():
            print("stdout: This should NOT be captured")
            sys.stderr.write("stderr: This should NOT be captured\n")
        print("stdout: This should be captured again")
        sys.stderr.write("stderr: This should be captured again\n")

        captured = capfd.readouterr()
        assert captured.out == "stdout: This should be captured\nstdout: This should be captured again\n"
        assert captured.err == "stderr: This should be captured\nstderr: This should be captured again\n"
