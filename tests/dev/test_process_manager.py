from unittest.mock import MagicMock, patch

from starui.dev.process_manager import ProcessManager


class TestProcessManager:
    def test_fresh_manager_has_no_running_processes(self):
        manager = ProcessManager()
        assert not manager.is_running("anything")
        assert not manager.shutdown.is_set()

    @patch("subprocess.Popen")
    def test_start_process_returns_existing_if_already_running(self, mock_popen):
        manager = ProcessManager()
        mock_proc = MagicMock()
        mock_proc.stdout.readline.return_value = ""
        mock_proc.poll.return_value = None
        mock_popen.return_value = mock_proc

        first = manager.start_process("test", ["cmd"])
        second = manager.start_process("test", ["cmd"])

        assert first is second
        # Popen should only have been called once
        mock_popen.assert_called_once()

    @patch("subprocess.Popen")
    def test_start_process_creates_and_tracks_new_process(self, mock_popen):
        manager = ProcessManager()
        mock_proc = MagicMock()
        mock_proc.stdout.readline.return_value = ""
        mock_proc.poll.return_value = None
        mock_popen.return_value = mock_proc

        result = manager.start_process("test", ["cmd"])

        assert result == mock_proc
        assert manager.is_running("test")

    def test_is_running_reflects_process_state(self):
        manager = ProcessManager()
        mock_proc = MagicMock()
        manager.processes["test"] = mock_proc

        # Process still alive (poll returns None)
        mock_proc.poll.return_value = None
        assert manager.is_running("test")

        # Process has exited (poll returns exit code)
        mock_proc.poll.return_value = 0
        assert not manager.is_running("test")

    def test_stop_process_terminates_and_removes(self):
        manager = ProcessManager()
        mock_proc = MagicMock()
        manager.processes["test"] = mock_proc

        manager.stop_process("test")

        mock_proc.terminate.assert_called_once()
        assert not manager.is_running("test")

    def test_stop_process_noop_for_unknown_name(self):
        manager = ProcessManager()

        # Should not raise
        result = manager.stop_process("nonexistent")
        assert result is True

    def test_stop_all_terminates_every_process(self):
        manager = ProcessManager()
        mock_procs = {f"test{i}": MagicMock() for i in range(3)}
        manager.processes = mock_procs.copy()

        manager.stop_all()

        assert manager.shutdown.is_set()
        for proc in mock_procs.values():
            proc.terminate.assert_called_once()

    def test_stop_all_is_idempotent(self):
        manager = ProcessManager()
        mock_proc = MagicMock()
        manager.processes["test"] = mock_proc

        manager.stop_all()
        manager.stop_all()  # Should not raise or double-terminate

        mock_proc.terminate.assert_called_once()
