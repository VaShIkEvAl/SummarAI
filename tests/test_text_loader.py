import io
from utils.text_loader import load_text_from_file

def test_load_text_from_file():
    fake_file = io.BytesIO(b"Hello World")
    result = load_text_from_file(fake_file)
    assert result == "Hello World"

def test_text_loader_non_empty():
    import io
    from utils.text_loader import load_text_from_file

    fake_file = io.BytesIO(b"Test Data")

    result = load_text_from_file(fake_file)

    assert len(result) > 0