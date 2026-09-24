#!/usr/bin/env python3
"""Build and serve a local Jekyll preview instead of opening source HTML."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import signal
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=0, help="local port; 0 picks an unused port")
    parser.add_argument("--site-dir", type=Path, help="serve an existing Jekyll build")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="pk-site-preview-") as temporary:
        output = args.site_dir.resolve() if args.site_dir else Path(temporary)
        if not args.site_dir:
            subprocess.run(["bash", str(ROOT / "scripts/build_site.sh"), str(output)], check=True, stdout=subprocess.DEVNULL)
        homepage = output / "index.html"
        html = homepage.read_text() if homepage.is_file() else ""
        if not html.lstrip().lower().startswith("<!doctype html>") or "{%" in html or "{{" in html:
            parser.error("--site-dir must contain a rendered Jekyll site, not source files")
        handler = partial(SimpleHTTPRequestHandler, directory=str(output))
        with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
            signal.signal(signal.SIGTERM, signal.default_int_handler)
            print(f"Preview: http://127.0.0.1:{server.server_port}/", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
