from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent_contract import build_agent_interface
from .csv_adapter import CsvImportError, import_csv_notices
from .generator import generate_notice, slug
from .io_utils import load_sample_request, read_json, write_json
from .models import ProductionNotice
from .profiles import profile_catalog
from .schedule_adapter import SchedulePlanError, generate_from_schedule
from .server import run_server
from .templates import NoticeTemplateError, build_notice_from_template, template_catalog
from .validation import validate_notice_payload


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="production-notice", description="Generate structured operations notice artifacts.")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("run-demo", help="Generate demo artifacts from synthetic sample data.")
    demo.add_argument("--output", default="output")
    demo.set_defaults(func=run_demo)

    generate = sub.add_parser("generate", help="Generate an operations notice from a JSON request.")
    generate.add_argument("--input", required=True)
    generate.add_argument("--output", default="output")
    generate.set_defaults(func=run_generate)

    validate = sub.add_parser("validate", help="Validate a notice request without writing artifacts.")
    validate.add_argument("--input", required=True)
    validate.set_defaults(func=run_validate)

    import_csv = sub.add_parser("import-csv", help="Convert work-package CSV rows into notice request JSON.")
    import_csv.add_argument("--input", required=True)
    output_target = import_csv.add_mutually_exclusive_group(required=True)
    output_target.add_argument("--output", help="Write one imported notice request to this JSON file.")
    output_target.add_argument("--output-dir", help="Write one JSON file per imported notice.")
    import_csv.set_defaults(func=run_import_csv)

    profiles = sub.add_parser("profiles", help="List built-in scenario profiles.")
    profiles.set_defaults(func=run_profiles)

    templates = sub.add_parser("templates", help="List built-in notice templates.")
    templates.add_argument("--template-file", help="Optional custom template file to merge into the catalog.")
    templates.set_defaults(func=run_templates)

    new_from_template = sub.add_parser("new-from-template", help="Create an editable notice request from a template.")
    new_from_template.add_argument("--template", required=True)
    new_from_template.add_argument("--output", required=True)
    new_from_template.add_argument("--template-file", help="Optional custom template file.")
    new_from_template.add_argument("--set", action="append", default=[], help="Override a field with dotted.path=value syntax.")
    new_from_template.add_argument("--custom-field", action="append", default=[], help="Add a custom field with key=value syntax.")
    new_from_template.set_defaults(func=run_new_from_template)

    schedule = sub.add_parser("schedule-generate", help="Generate notice requests and artifacts from a schedule plan.")
    schedule.add_argument("--input", required=True)
    schedule.add_argument("--output", required=True)
    schedule.add_argument("--template-file", help="Optional custom template file.")
    schedule.set_defaults(func=run_schedule_generate)

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
    serve.add_argument("--allow-remote", action="store_true", help="Allow binding to non-loopback hosts.")
    serve.set_defaults(func=run_serve)

    args = parser.parse_args(argv)
    args.func(args)


def run_demo(args: argparse.Namespace) -> None:
    result = generate_notice(load_sample_request(), args.output)
    print(json.dumps(result.as_manifest(), indent=2))


def run_generate(args: argparse.Namespace) -> None:
    result = generate_notice(read_json(args.input), args.output)
    print(json.dumps(result.as_manifest(), indent=2))


def run_validate(args: argparse.Namespace) -> None:
    result = validate_notice_payload(read_json(args.input))
    print(json.dumps(result.as_dict(), ensure_ascii=False, indent=2))
    if not result.ok:
        raise SystemExit(1)


def run_import_csv(args: argparse.Namespace) -> None:
    try:
        notices = import_csv_notices(args.input)
    except CsvImportError as exc:
        raise SystemExit(str(exc)) from exc

    if args.output:
        if len(notices) != 1:
            raise SystemExit("Use --output-dir when importing a CSV with multiple notice_id values")
        path = write_json(args.output, notices[0])
        print(json.dumps({"count": 1, "files": [str(path)]}, indent=2))
        return

    output_dir = Path(args.output_dir)
    files = []
    for payload in notices:
        filename = f"{slug(str(payload['notice_id']))}.json"
        files.append(str(write_json(output_dir / filename, payload)))
    print(json.dumps({"count": len(files), "files": files}, indent=2))


def run_profiles(args: argparse.Namespace) -> None:
    print(json.dumps(profile_catalog(), ensure_ascii=False, indent=2))


def run_templates(args: argparse.Namespace) -> None:
    try:
        catalog = template_catalog(args.template_file)
    except NoticeTemplateError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(catalog, ensure_ascii=False, indent=2))


def run_new_from_template(args: argparse.Namespace) -> None:
    try:
        payload = build_notice_from_template(
            args.template,
            template_file=args.template_file,
            overrides=args.set,
            custom_fields=args.custom_field,
        )
    except NoticeTemplateError as exc:
        raise SystemExit(str(exc)) from exc
    path = write_json(args.output, payload)
    print(path)


def run_schedule_generate(args: argparse.Namespace) -> None:
    try:
        manifest = generate_from_schedule(args.input, args.output, template_file=args.template_file)
    except (SchedulePlanError, NoticeTemplateError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


def run_analysis_context(args: argparse.Namespace) -> None:
    notice = ProductionNotice.from_dict(read_json(args.input))
    path = write_json(args.output, notice.to_agent_context())
    print(path)


def run_agent_spec(args: argparse.Namespace) -> None:
    path = write_json(Path(args.output), build_agent_interface())
    print(path)


def run_serve(args: argparse.Namespace) -> None:
    run_server(args.host, args.port, args.output, allow_remote=args.allow_remote)


if __name__ == "__main__":
    main()
