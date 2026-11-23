import pytest
from fastapi import HTTPException

from backend.api.report import ReportRequest, generate_report


def _request(filename: str) -> ReportRequest:
    return ReportRequest(
        filename=filename,
        prediction="prediction",
        protected="gender",
        predict_url="https://example.com/predict",
    )


@pytest.mark.parametrize(
    "bad",
    [
        "../../etc/passwd",
        "a/b.csv",
        "..\\secret",
        "nested/dir/file.csv",
    ],
)
def test_report_rejects_traversal_filenames(bad):
    with pytest.raises(HTTPException) as exc_info:
        generate_report(_request(bad))
    assert exc_info.value.status_code == 400
