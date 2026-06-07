from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent_contract import build_agent_interface
from .generator import generate_notice
from .io_utils import load_sample_request, read_json, write_json
from .models import ProductionNotice
from .server import run_server


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="production-notice")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("run-demo", help="Generate demo artifacts from synthetic sample data.")
    demo.add_argument("--output", default="output")
    demo.set_defaults(func=run_demo)

    generate = sub.add_parser("generate", help="Generate a production notice from a JSON request.")
    generate.add_argument("--input", required=True)
    generate.add_argument("--output", default="output")
    generate.set_defaults(func=run_generate)

    context = sub.add_parser("analysis-context", help="Export structured context for downstream agents.")
    context.add_argument("--input", required=True)
    context.add_argument("--output", required=True)
    context.set_defaults(func=run_analysis_context)

    spec = sub.add_parser("agent-spec", help="Write the machine-readable agent interface.")
    spec.add_argument("--output", default="agent_interface.json")
    spec.set_defaults(func=run_agent_spec)

    serve = sub.add_parser("serve", help="Run a small local JSON API for agent integration demos.")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--output", default="output")
    serve.set_defaults(func=run_serve)

    args = parser.parse_args(argv)
    args.func(args)


def run_demo(args: argparse.Namespace) -> None:
    result = generate_notice(load_sample_request(), args.output)
    print(json.dumps(result.as_manifest(), indent=2))


def run_generate(args: argparse.Namespace) -> None:
    result = generate_notice(read_json(args.input), args.output)
    print(json.dumps(result.as_manifest(), indent=2))


def run_analysis_context(args: argparse.Namespace) -> None:
    notice = ProductionNotice.from_dict(read_json(args.input))
    path = write_json(args.output, notice.to_agent_context())
    print(path)


def run_agent_spec(args: argparse.Namespace) -> None:
    path = write_json(Path(args.output), build_agent_interface())
    print(path)


def run_serve(args: argparse.Namespace) -> None:
    run_server(args.host, args.port, args.output)


if __name__ == "__main__":
    main()
