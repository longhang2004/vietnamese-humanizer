from pathlib import Path

if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent / "src/vietnamese_writing_skills/cli/dev.py"
    __import__("runpy").run_path(str(path), run_name="__main__")
