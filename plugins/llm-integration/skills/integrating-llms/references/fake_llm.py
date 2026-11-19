"""A stand-in OpenAI-compatible AI: try the UI end to end, or run tests, without a key or network.

Run: python tests/fake_llm.py 8799, then set LLM_PROVIDER=openai, LLM_BASE_URL=http://127.0.0.1:8799/v1,
LLM_MODEL=fake. It picks the canned reply whose prompt file's first line appears in the system message,
so each prompt in prompts/<name>.md must start with a line unique to that task.

Pair with this autouse fixture in tests/conftest.py, so no test reaches a developer's running Ollama:

    @pytest.fixture(autouse=True)
    def no_real_local_ai(monkeypatch):
        from myapp import llm
        monkeypatch.setattr(llm, "LOCAL_URL", "http://127.0.0.1:9/v1")  # discard port: nothing answers

Canned replies must pass the app's own validators and cross-checks (write a test that asserts this).
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PROMPTS = Path(__file__).resolve().parents[1] / "myapp" / "prompts"  # adapt
REPLIES = {  # prompt name -> the JSON the model would return; adapt to the app's schemas
    "extract": {"title": "Example record", "summary": "One line", "deadline": None},
    "filter": {"picks": [], "discarded": 0},
}
DEFAULT = "filter"


def first_line(name: str) -> str:
    return (PROMPTS / f"{name}.md").read_text(encoding="utf-8").splitlines()[0]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        system = next((m["content"] for m in body.get("messages", []) if m["role"] == "system"), "")
        name = next((n for n in REPLIES if first_line(n) in system), DEFAULT)
        out = json.dumps({"choices": [{"message": {"content": json.dumps(REPLIES[name], ensure_ascii=False)}}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)


def make_server(port: int) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    make_server(int(sys.argv[1]) if len(sys.argv) > 1 else 8799).serve_forever()
