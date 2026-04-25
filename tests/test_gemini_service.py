# ================= IMPORTS =================
import json
from services import gemini_service

# ================= HELPER CLASS =================
class FakeResponse:
    def __init__(self, text):
        self.text = text


# ================= PART A: HELPER FUNCTIONS =================
def test_split_text_smart():
    text = "Hello. How are you? I am fine."
    chunks = gemini_service.split_text_smart(text, max_chars=20)
    assert len(chunks) >= 1


def test_add_overlap():
    chunks = ["Hello world", "How are you"]
    result = gemini_service.add_overlap(chunks, overlap_size=5)
    assert len(result) == 2
    assert result[1].startswith("world")


def test_remove_duplicates():
    items = ["a", "b", "a"]
    result = gemini_service.remove_duplicates(items)
    assert result == ["a", "b"]


# ================= PART B: SUCCESS CASE =================
def test_generate_summary_success(monkeypatch):

    def fake_generate_content(self, prompt):
        return FakeResponse(json.dumps({
            "title": "Test",
            "summary": "Test summary",
            "key_points": ["point1"],
            "action_items": ["task1"]
        }))

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.generate_summary("Hello world")

    assert "summary" in result


# ================= PART C: JSON FAILURE =================
def test_generate_summary_json_fail(monkeypatch):

    def fake_generate_content(self, prompt):
        return FakeResponse("INVALID JSON")

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.generate_summary("Hello world")

    assert "summary" in result


# ================= PART D: QA FUNCTION =================
def test_answer_all_questions(monkeypatch):

    def fake_generate_content(self, prompt):
        return FakeResponse('[{"question":"Q1","answer":"A1"}]')

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.answer_all_questions("summary", ["Q1"])

    assert "Q1" in result


def test_summary_exact(monkeypatch):
    class FakeResponse:
        def __init__(self, text):
            self.text = text

    def fake_generate_content(self, prompt):
        return FakeResponse('{"summary":"correct","key_points":["p1"],"action_items":["a1"]}')

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.generate_summary("Hello")

    assert result["summary"] == "correct"

def test_summary_exact(monkeypatch):
    class FakeResponse:
        def __init__(self, text):
            self.text = text

    def fake_generate_content(self, prompt):
        return FakeResponse('{"summary":"correct","key_points":["p1"],"action_items":["a1"]}')

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.generate_summary("Hello")

    assert result["summary"] == "correct"

def test_keypoints_strict(monkeypatch):
    class FakeResponse:
        def __init__(self, text):
            self.text = text

    def fake_generate_content(self, prompt):
        return FakeResponse('{"summary":"ok","key_points":["p1","p2"],"action_items":["a1"]}')

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.generate_summary("Hello")

    assert result["key_points"] == ["p1","p2"]

def test_multi_chunk_strict(monkeypatch):
    class FakeResponse:
        def __init__(self, text):
            self.text = text

    def fake_generate_content(self, prompt):
        return FakeResponse('{"summary":"chunk","key_points":["p"],"action_items":["a"]}')

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    text = "Sentence. " * 200

    result = gemini_service.generate_summary(text)

    assert len(result["summary"]) > 0

def test_fallback_values(monkeypatch):
    class FakeResponse:
        def __init__(self, text):
            self.text = text

    def fake_generate_content(self, prompt):
        return FakeResponse("INVALID JSON")

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.generate_summary("Hello")

    assert isinstance(result["key_points"], list)
    assert isinstance(result["action_items"], list)

def test_keypoints_not_empty(monkeypatch):
    class FakeResponse:
        def __init__(self, text):
            self.text = text

    def fake_generate_content(self, prompt):
        return FakeResponse('{"summary":"ok","key_points":["p1"],"action_items":["a1"]}')

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.generate_summary("Hello")

    assert len(result["key_points"]) > 0

def test_action_items_not_empty(monkeypatch):
    class FakeResponse:
        def __init__(self, text):
            self.text = text

    def fake_generate_content(self, prompt):
        return FakeResponse('{"summary":"ok","key_points":["p1"],"action_items":["a1"]}')

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.generate_summary("Hello")

    assert len(result["action_items"]) > 0

# def test_summary_not_constant(monkeypatch):
#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse('{"summary":"' + prompt[:10] + '","key_points":["p"],"action_items":["a"]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Different input text")

#     assert len(result["summary"]) > 0

def test_combined_summary_not_empty(monkeypatch):
    class FakeResponse:
        def __init__(self, text):
            self.text = text

    def fake_generate_content(self, prompt):
        return FakeResponse('{"summary":"final","key_points":["p"],"action_items":["a"]}')

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.generate_summary("Hello")

    assert result["summary"] != ""

def test_full_structure(monkeypatch):
    class FakeResponse:
        def __init__(self, text):
            self.text = text

    def fake_generate_content(self, prompt):
        return FakeResponse('{"summary":"ok","key_points":["p"],"action_items":["a"]}')

    monkeypatch.setattr(
        gemini_service.genai.GenerativeModel,
        "generate_content",
        fake_generate_content
    )

    result = gemini_service.generate_summary("Hello")

    assert "summary" in result
    assert "key_points" in result
    assert "action_items" in result
#
#  # ================= IMPORTS =================
# import json
# from services import gemini_service

# # ================= HELPER CLASS =================
# class FakeResponse:
#     def __init__(self, text):
#         self.text = text


# # ================= PART A: HELPER FUNCTIONS =================
# def test_split_text_smart():
#     text = "Hello. How are you? I am fine."
#     chunks = gemini_service.split_text_smart(text, max_chars=20)
#     assert len(chunks) >= 1


# def test_add_overlap():
#     chunks = ["Hello world", "How are you"]
#     result = gemini_service.add_overlap(chunks, overlap_size=5)
#     assert len(result) == 2
#     assert result[1].startswith("world")


# def test_remove_duplicates():
#     items = ["a", "b", "a"]
#     result = gemini_service.remove_duplicates(items)
#     assert result == ["a", "b"]


# # ================= PART B: SUCCESS CASE =================
# def test_generate_summary_success(monkeypatch):

#     def fake_generate_content(self, prompt):
#         return FakeResponse(json.dumps({
#             "title": "Test",
#             "summary": "Test summary",
#             "key_points": ["point1"],
#             "action_items": ["task1"]
#         }))

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello world")

#     assert "summary" in result

# def test_summary_not_empty(monkeypatch):
#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse('{"summary":"valid","key_points":["p1"],"action_items":["a1"]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello")

#     assert result["summary"] != ""

# # ================= PART C: JSON FAILURE =================
# def test_generate_summary_json_fail(monkeypatch):

#     def fake_generate_content(self, prompt):
#         return FakeResponse("INVALID JSON")

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello world")

#     assert "summary" in result

# def test_generate_summary_final_json_fail(monkeypatch):

#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     call_count = {"count": 0}

#     def fake_generate_content(self, prompt):
#         call_count["count"] += 1

#         # First call → valid JSON (chunk stage)
#         if call_count["count"] == 1:
#             return FakeResponse('{"summary":"partial","key_points":["p1"],"action_items":["a1"]}')
        
#         # Final call → invalid JSON (triggers fallback)
#         return FakeResponse("INVALID FINAL JSON")

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello world")

#     assert "summary" in result

# def test_generate_summary_markdown_cleanup(monkeypatch):

#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse(
#             "```json {\"summary\":\"ok\",\"key_points\":[],\"action_items\":[]} ```"
#         )

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello world")

#     assert "summary" in result

# def test_summary_contains_key_points(monkeypatch):

#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse('{"summary":"ok","key_points":["p1"],"action_items":["a1"]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello world")

#     assert len(result["key_points"]) > 0

# def test_summary_contains_action_items(monkeypatch):

#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse('{"summary":"ok","key_points":["p1"],"action_items":["a1"]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello world")

#     assert len(result["action_items"]) > 0

# def test_summary_exact_match(monkeypatch):
#     from services import gemini_service

#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse('{"summary":"meeting summary","key_points":["p1"],"action_items":["a1"]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello")

#     assert result["summary"] == "meeting summary"

# def test_keypoints_exact(monkeypatch):
#     from services import gemini_service

#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse('{"summary":"ok","key_points":["p1","p2"],"action_items":["a1"]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello")

#     assert result["key_points"] == ["p1","p2"]

# def test_action_items_exact(monkeypatch):
#     from services import gemini_service

#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse('{"summary":"ok","key_points":["p1"],"action_items":["a1","a2"]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello")

#     assert result["action_items"] == ["a1","a2"]

# def test_generate_summary_multiple_chunks(monkeypatch):
#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse('{"summary":"chunk","key_points":["p"],"action_items":["a"]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     long_text = "Sentence. " * 100

#     result = gemini_service.generate_summary(long_text)

#     assert "summary" in result

# def test_generate_summary_empty_input(monkeypatch):
#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse('{"summary":"","key_points":[],"action_items":[]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("")

#     assert "summary" in result

# def test_duplicate_removal_effect(monkeypatch):
#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse('{"summary":"ok","key_points":["p1","p1"],"action_items":["a1","a1"]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Hello")

#     # Instead of strict equality, check duplicates are reduced
#     assert len(result["key_points"]) <= 2

# def test_invalid_chunk_skipped(monkeypatch):
#     from services import gemini_service

#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     call_count = {"count": 0}

#     def fake_generate_content(self, prompt):
#         call_count["count"] += 1
#         if call_count["count"] == 1:
#             return FakeResponse("INVALID JSON")  # triggers continue
#         return FakeResponse('{"summary":"ok","key_points":[],"action_items":[]}')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.generate_summary("Sentence. Another sentence.")

#     assert "summary" in result

# def test_add_overlap_nonzero():
#     from services import gemini_service

#     chunks = ["First chunk text", "Second chunk text"]

#     result = gemini_service.add_overlap(chunks, overlap_size=5)

#     assert len(result) == 2
#     assert result[1] != chunks[1]

# # ================= PART D: QA FUNCTION =================
# def test_answer_all_questions_empty(monkeypatch):

#     class FakeResponse:
#         def __init__(self, text):
#             self.text = text

#     def fake_generate_content(self, prompt):
#         return FakeResponse("[]")

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.answer_all_questions("summary", ["Q1"])

#     assert result is not None

# def test_answer_all_questions(monkeypatch):

#     def fake_generate_content(self, prompt):
#         return FakeResponse('[{"question":"Q1","answer":"A1"}]')

#     monkeypatch.setattr(
#         gemini_service.genai.GenerativeModel,
#         "generate_content",
#         fake_generate_content
#     )

#     result = gemini_service.answer_all_questions("summary", ["Q1"])

#     assert "Q1" in result