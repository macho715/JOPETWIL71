#!/usr/bin/env python3
from __future__ import annotations

import argparse
import http.server
import socketserver
import threading
import time
import webbrowser
from pathlib import Path


DEFAULT_DASHBOARD = Path("DASHBOARD/JPT71_Voyage_KPI_Dashboard_v4.html")
DEFAULT_PORT = 8771


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serve and open the JPT71 v4 KPI dashboard locally."
    )
    parser.add_argument(
        "--dashboard",
        type=Path,
        default=DEFAULT_DASHBOARD,
        help="Relative or absolute path to the HTML dashboard file.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Local HTTP port to use.",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Start the local server without opening a browser tab.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    dashboard_path = (repo_root / args.dashboard).resolve()

    if not dashboard_path.exists():
        print(f"Dashboard not found: {dashboard_path}")
        return 1

    try:
        rel_dashboard = dashboard_path.relative_to(repo_root).as_posix()
    except ValueError:
        print("Dashboard must be inside the current workspace.")
        return 1

    handler = http.server.SimpleHTTPRequestHandler
    with ReusableTCPServer(("127.0.0.1", args.port), handler) as httpd:
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()

        url = f"http://127.0.0.1:{args.port}/{rel_dashboard}"
        print(f"Serving: {repo_root}")
        print(f"Dashboard: {dashboard_path}")
        print(f"Open: {url}")

        if not args.no_browser:
            webbrowser.open(url)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping server...")
        finally:
            httpd.shutdown()
            httpd.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
