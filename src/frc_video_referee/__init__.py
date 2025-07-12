"""
FRC Video Referee - Video analysis and referee assistance for FRC competitions.
"""

import argparse
import sys


def main() -> None:
    """Main entry point for the FRC Video Referee application."""
    parser = argparse.ArgumentParser(description="FRC Video Referee Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload for development"
    )

    args = parser.parse_args()

    try:
        from .server import run_server

        print(f"Starting FRC Video Referee server on {args.host}:{args.port}")
        run_server(host=args.host, port=args.port, reload=args.reload)
    except ImportError as e:
        print(f"Error importing server: {e}")
        print("Please install the required dependencies with: uv sync")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0)
