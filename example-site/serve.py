import http.server
import socketserver
import sys
import webbrowser
from pathlib import Path
from typing import Any


def serve_site(serve_dir_str: str) -> None:
    """Serves the specified directory."""
    # Resolve the path relative to the current working directory
    # as the script is likely run from the project root.
    serve_dir = Path(serve_dir_str).resolve()

    if not serve_dir.is_dir():
        print(f"Error: Directory '{serve_dir}' not found.")
        sys.exit(1)

    port = 8080
    # Use 0.0.0.0 to make it accessible on the network if needed
    server_address = "0.0.0.0", port  # noqa: S104
    url = f"http://localhost:{port}/"  # Still open localhost for convenience

    # Create a handler that serves files from the specified directory
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize the handler with the specified directory."""
            super().__init__(*args, directory=str(serve_dir), **kwargs)

    print(f"Serving directory '{serve_dir}' at {url}")

    # Check if port is already in use
    try:
        # Use the custom handler
        with socketserver.TCPServer(server_address, Handler) as httpd:
            webbrowser.open(url)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nStopping server...")
                httpd.server_close()
    except OSError as e:
        if "address already in use" in str(e):
            print(
                f"Error: Port {port} is already in use. Please stop the other process or choose a different port."
            )
        else:
            print(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python serve.py <directory_to_serve>")
        sys.exit(1)

    directory_to_serve = sys.argv[1]
    serve_site(directory_to_serve)
