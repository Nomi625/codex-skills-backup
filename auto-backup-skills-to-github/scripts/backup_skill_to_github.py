#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path


DEFAULT_SKILLS_ROOTS = [
    Path(r"C:\Users\Administrator\.codex\skills"),
    Path(r"C:\Users\Administrator\.agents\skills"),
]
DEFAULT_REPO = Path(r"C:\Users\Administrator\Documents\codex-skills-backup")
DEFAULT_OBSIDIAN_DIR = Path(r"C:\Users\Administrator\Desktop\LabNotes\Skills管理")


def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result


def find_skill(skill_name, skills_roots):
    if skill_name == ".system" or skill_name.startswith("."):
        raise ValueError("Refusing to back up system or hidden skill directories")
    for skills_root in skills_roots:
        source = skills_root / skill_name
        if (source / "SKILL.md").exists():
            return source
    checked = ", ".join(str(root / skill_name) for root in skills_roots)
    raise FileNotFoundError(f"Missing skill source. Checked: {checked}")


def copy_skill(skill_name, skills_roots, repo):
    source = find_skill(skill_name, skills_roots)
    target = repo / skill_name
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


def read_skill_description(skill_dir):
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return ""
    for line in skill_file.read_text(encoding="utf-8", errors="replace").splitlines()[:30]:
        if line.startswith("description:"):
            return line.replace("description:", "", 1).strip().strip('"')
    return ""


def copy_skill_to_obsidian(skill_name, source, obsidian_dir):
    obsidian_dir.mkdir(parents=True, exist_ok=True)
    target = obsidian_dir / skill_name
    if target.exists():
        shutil.rmtree(target)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", ".git")
    shutil.copytree(source, target, ignore=ignore)
    return target


def update_obsidian_index(obsidian_dir, source_label):
    skills = []
    for child in sorted(obsidian_dir.iterdir(), key=lambda p: p.name.lower()):
        if child.is_dir():
            skills.append((child.name, read_skill_description(child)))

    lines = [
        "# Codex Skills 管理",
        "",
        "这个文件夹是本地 skills 镜像。GitHub 打不开时，可以在这里查看、搜索和管理 skill。",
        "",
        f"来源：`{source_label}`",
        "",
        "## 使用方式",
        "",
        "- 每个子文件夹是一个 skill。",
        "- 主要说明文件通常是 `SKILL.md`。",
        "- 详细资料在各 skill 的 `references/`、`scripts/` 或 `agents/` 中。",
        "- 真正让 Codex 自动发现的安装位置仍是 `C:\\Users\\Administrator\\.codex\\skills`。",
        "",
        "## Skills 列表",
        "",
    ]
    for name, description in skills:
        link = f"[[Skills管理/{name}/SKILL|{name}]]"
        if description:
            lines.append(f"- {link} - {description}")
        else:
            lines.append(f"- {link}")
    (obsidian_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(skills)


def main():
    parser = argparse.ArgumentParser(description="Copy a Codex or agent skill into the GitHub backup repo.")
    parser.add_argument("--skill-name", required=True)
    parser.add_argument(
        "--skills-root",
        action="append",
        default=None,
        help="Skill root to search. Can be passed multiple times.",
    )
    parser.add_argument("--repo", default=str(DEFAULT_REPO))
    parser.add_argument("--obsidian-dir", default=str(DEFAULT_OBSIDIAN_DIR))
    parser.add_argument("--no-obsidian", action="store_true", help="Do not mirror the skill into Obsidian")
    parser.add_argument("--commit-message", default=None)
    parser.add_argument("--commit", action="store_true", help="Run git add/commit after copying")
    parser.add_argument("--push", action="store_true", help="Run git push after committing")
    args = parser.parse_args()

    skills_roots = [Path(root) for root in args.skills_root] if args.skills_root else DEFAULT_SKILLS_ROOTS
    repo = Path(args.repo)
    skill_name = args.skill_name
    commit_message = args.commit_message or f"Add {skill_name} skill"

    source, target = copy_skill(skill_name, skills_roots, repo)
    readme_changed = update_readme(skill_name, repo)

    print(f"Copied {source} -> {target}")
    if readme_changed:
        print("Updated README.md")

    if not args.no_obsidian:
        obsidian_target = copy_skill_to_obsidian(skill_name, source, Path(args.obsidian_dir))
        count = update_obsidian_index(Path(args.obsidian_dir), str(repo))
        print(f"Copied {source} -> {obsidian_target}")
        print(f"Updated Obsidian skills index ({count} skills)")

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
