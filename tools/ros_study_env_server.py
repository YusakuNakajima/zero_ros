#!/usr/bin/env python3
import json
import shutil
import subprocess
import threading
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'environment-setup' / 'index.html'
ACTIONS = {
    'build-up': ['docker', 'compose', '-f', 'docker/compose.yaml', 'up', '--build', '-d', '--remove-orphans'],
    'compose-logs': ['docker', 'compose', '-f', 'docker/compose.yaml', 'logs', '--no-color', '--tail', '200'],
    'down': ['docker', 'compose', '-f', 'docker/compose.yaml', 'down', '--remove-orphans'],
}


class EnvState:
    def __init__(self):
        self.lock = threading.Lock()
        self.busy = False
        self.current_action = None
        self.last_action = None
        self.exit_code = None
        self.logs = deque(maxlen=4000)

    def append(self, line: str) -> None:
        with self.lock:
            self.logs.append(line.rstrip('\n'))

    def snapshot(self) -> dict:
        with self.lock:
            return {
                'busy': self.busy,
                'current_action': self.current_action,
                'last_action': self.last_action,
                'exit_code': self.exit_code,
                'logs': '\n'.join(self.logs),
            }

    def start(self, action: str) -> bool:
        with self.lock:
            if self.busy:
                return False
            self.busy = True
            self.current_action = action
            self.last_action = action
            self.exit_code = None
            self.logs.clear()
        return True

    def finish(self, code: int) -> None:
        with self.lock:
            self.busy = False
            self.exit_code = code
            self.current_action = None


STATE = EnvState()


def run_action(action_name: str):
    if action_name not in ACTIONS:
        return False, 'unknown action'
    if not STATE.start(action_name):
        return False, 'another action is already running'

    command = ACTIONS[action_name]
    STATE.append(f"$ {' '.join(command)}")
    if shutil.which('docker') is None:
        STATE.append('[helper] docker command was not found on this machine.')
        STATE.finish(127)
        return True, None

    def worker() -> None:
        try:
            process = subprocess.Popen(
                command,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            assert process.stdout is not None
            for line in process.stdout:
                STATE.append(line)
            code = process.wait()
            STATE.append('')
            STATE.append(f'[helper] command finished with exit code {code}')
            STATE.finish(code)
        except Exception as exc:  # pragma: no cover - local helper path
            STATE.append('')
            STATE.append(f'[helper] error: {exc}')
            STATE.finish(1)

    threading.Thread(target=worker, daemon=True).start()
    return True, None


class Handler(BaseHTTPRequestHandler):
    def _cors(self) -> None:
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _write_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ('/', '/index.html', '/environment-setup/', '/environment-setup/index.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self._cors()
            self.end_headers()
            self.wfile.write(PAGE.read_bytes())
            return
        if parsed.path == '/api/state':
            self._write_json(200, STATE.snapshot())
            return
        self.send_response(404)
        self._cors()
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith('/api/actions/'):
            action = parsed.path.split('/')[-1]
            ok, error = run_action(action)
            self._write_json(200 if ok else 409, {'ok': ok, 'error': error})
            return
        self.send_response(404)
        self._cors()
        self.end_headers()

    def log_message(self, fmt, *args):
        return


def main() -> None:
    server = ThreadingHTTPServer(('127.0.0.1', 8765), Handler)
    print('ros_study env helper listening on http://127.0.0.1:8765')
    print('Open environment-setup/index.html or the URL above in your browser.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
