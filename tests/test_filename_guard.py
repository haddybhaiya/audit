import pytest

from backend.data_layer.dataset_loader import validate_dataset_filename


@pytest.mark.parametrize(
    "bad",
    [
        "../escape.csv",
        "a/b.csv",
        "/etc/passwd",
        "..\\secret",
        "a\\b.csv",
        "nested/dir/file.csv",
    ],
)
def test_rejects_filenames_with_separators(bad):
    with pytest.raises(ValueError):
        validate_dataset_filename(bad)


@pytest.mark.parametrize(
    "good",
    [
        "abc123def_file.csv",
        "normal_name.csv",
        "uuid_prefix_file.csv",
    ],
)
def test_accepts_plain_filenames(good):
    validate_dataset_filename(good)
