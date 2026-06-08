#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path


DEFAULT_SKILLS_ROOT = Path(r"C:\Users\Administrator\.codex\skills")
DEFAULT_REPO = Path(r"C:\Users\Administrator\Documents\codex-skills-backup")


def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result


def copy_skill(skill_name, skills_root, repo):
    if skill_name == ".system" or skill_name.startswith("."):
        raise ValueError("Refusing to back up system or hidden skill directories")
    source = skills_root / skill_name
    target = repo / skill_name
    if not (source / "SKILL.md").exists():
        raise FileNotFoundError(f"Missing skill source: {source}")
    if target.exists():
        shutil.rmtree(target)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
    shutil.copytree(source, target, ignore=ignore)
    return source, target


def update_readme(skill_name, repo):
    readme = repo / "README.md"
    if not readme.exists():
        return False
    text = readme.read_text(encoding="utf-8")
    bullet = f"- `{skill_name}`"
    if bullet in text:
        return False
    marker = "- Shared reference files in `_shared`"
    if marker in text:
        text = text.replace(marker, f"{bullet}\n{marker}")
    else:
        text = text.rstrip() + f"\n\n{bullet}\n"
    readme.write_text(text, encoding="utf-8", newline="\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="Copy a Codex skill into the GitHub backup repo.")
    parser.add_argument("--skill-name", required=True)
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT))
    parser.add_argument("--repo", default=str(DEFAULT_REPO))
    parser.add_argument("--commit-message", default=None)
    parser.add_argument("--commit", action="store_true", help="Run git add/commit after copying")
    parser.add_argument("--push", action="store_true", help="Run git push after committing")
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    repo = Path(args.repo)
    skill_name = args.skill_name
    commit_message = args.commit_message or f"Add {skill_name} skill"

    source, target = copy_skill(skill_name, skills_root, repo)
    readme_changed = update_readme(skill_name, repo)

    print(f"Copied {source} -> {target}")
    if readme_changed:
        print("Updated README.md")

    status = run(["git", "status", "--short"], cwd=repo, check=False)
    print(status.stdout.strip())

    if args.commit:
        run(["git", "add", "README.md", skill_name], cwd=repo)
        run(["git", "commit", "-m", commit_message], cwd=repo)
        print(f"Committed: {commit_message}")
    else:
        print(f"Next: git add README.md {skill_name}")
        print(f"Next: git commit -m \"{commit_message}\"")

    if args.push:
        if not args.commit:
            raise ValueError("--push requires --commit")
        run(["git", "push", "origin", "master"], cwd=repo)
        print("Pushed origin master")
    elif args.commit:
        print("Next: git push origin master")


if __name__ == "__main__":
    raise SystemExit(main())
