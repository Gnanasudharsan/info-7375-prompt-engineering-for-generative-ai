"""CLI: python -m jobwatch watch [--from-file PATH] [--root DIR] [--no-claude] [--prompt PATH]"""
import argparse
from datetime import datetime, timezone
from pathlib import Path

from . import claude_judge
from .persona import DEFAULT_PERSONA, load_persona
from .watch import format_summary, run_watch

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="jobwatch")
    sub = parser.add_subparsers(dest="command", required=True)
    watch = sub.add_parser("watch", help="diff the Anthropic Greenhouse board against state")
    watch.add_argument("--from-file", type=Path,
                       help="use a saved raw response instead of fetching (labeled SEEDED)")
    watch.add_argument("--root", type=Path,
                       help="directory holding state/ and data/ (default: project folder, "
                            "or project seeded/ folder with --from-file)")
    watch.add_argument("--persona", type=Path, default=DEFAULT_PERSONA)
    watch.add_argument("--no-claude", action="store_true",
                       help="rule judge only; needs no ANTHROPIC_API_KEY")
    watch.add_argument("--prompt", type=Path, default=claude_judge.DEFAULT_PROMPT,
                       help="Claude judge prompt file (model from JOBWATCH_MODEL)")
    args = parser.parse_args(argv)

    root = args.root
    if args.from_file is not None:
        # Seeded runs never read or write the project's own state/ or data/runs/.
        if root is None:
            root = PROJECT_ROOT / "seeded"
        if root.resolve() == PROJECT_ROOT.resolve():
            parser.error("--from-file cannot use the project folder as --root")
    elif root is None:
        root = PROJECT_ROOT

    # CONTRACT.md: the résumé must pass its checks before anything runs.
    persona = load_persona(args.persona)
    judge = None
    if not args.no_claude:
        try:
            judge = claude_judge.make_judge(args.prompt)
        except claude_judge.ClaudeJudgeUnavailable as exc:
            parser.error(str(exc))
    report = run_watch(root, datetime.now(timezone.utc), from_file=args.from_file,
                       persona=persona, claude_judge=judge)
    print(format_summary(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
