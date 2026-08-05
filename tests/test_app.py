import ast
from pathlib import Path


def test_app_syntax():
    p = Path(__file__).parents[1] / "app.py"
    code = p.read_text(encoding="utf-8")
    ast.parse(code)


def test_contains_title_and_button():
    p = Path(__file__).parents[1] / "app.py"
    code = p.read_text(encoding="utf-8")
    assert "AI Code Explainer" in code
    assert "Explain Code" in code or "Explain this code" in code or "🚀 Explain Code" in code


def test_mentions_ollama():
    p = Path(__file__).parents[1] / "app.py"
    code = p.read_text(encoding="utf-8")
    assert "ollama" in code
