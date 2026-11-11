from scheduler.paths import PROJECT_ROOT, resolve_project_path
from scheduler.solver import load_data
from scheduler.utils import get_static_version


def test_project_paths_are_anchored_not_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert resolve_project_path("data/patients.json") == PROJECT_ROOT / "data/patients.json"
    nurses, patients, history = load_data()
    assert nurses
    assert patients
    assert history is not None
    assert get_static_version() != "unknown"
