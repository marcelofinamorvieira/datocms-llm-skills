#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  apply_with_rollback.sh \
    --repo-root /abs/repo \
    --files /abs/file1,/abs/file2 \
    --change-cmd "<mutating command>" \
    --validate-cmd "<validation command>"
USAGE
}

repo_root=""
files_csv=""
change_cmd=""
validate_cmd=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root)
      repo_root="$2"
      shift 2
      ;;
    --files)
      files_csv="$2"
      shift 2
      ;;
    --change-cmd)
      change_cmd="$2"
      shift 2
      ;;
    --validate-cmd)
      validate_cmd="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$repo_root" || -z "$files_csv" || -z "$change_cmd" || -z "$validate_cmd" ]]; then
  usage >&2
  exit 2
fi

IFS=',' read -r -a files <<< "$files_csv"
if [[ "${#files[@]}" -eq 0 ]]; then
  echo "No files provided" >&2
  exit 2
fi

backup_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$backup_dir"
}
trap cleanup EXIT

restore_all() {
  for file in "${files[@]}"; do
    rel="${file#${repo_root}/}"
    backup_file="$backup_dir/$rel"
    if [[ -f "$backup_file" ]]; then
      mkdir -p "$(dirname "$file")"
      cp "$backup_file" "$file"
    else
      rm -f "$file"
    fi
  done
}

for file in "${files[@]}"; do
  if [[ "$file" != "$repo_root"/* ]]; then
    echo "Refusing to edit file outside repo root: $file" >&2
    exit 2
  fi

  rel="${file#${repo_root}/}"
  backup_file="$backup_dir/$rel"
  mkdir -p "$(dirname "$backup_file")"
  if [[ -f "$file" ]]; then
    cp "$file" "$backup_file"
  fi
done

set +e
bash -lc "$change_cmd"
change_status=$?
set -e
if [[ $change_status -ne 0 ]]; then
  restore_all
  echo "APPLY_WITH_ROLLBACK: FAIL" >&2
  echo "ROLLED_BACK: true" >&2
  echo "REASON: change command failed" >&2
  exit $change_status
fi

set +e
bash -lc "$validate_cmd"
validate_status=$?
set -e
if [[ $validate_status -ne 0 ]]; then
  restore_all
  echo "APPLY_WITH_ROLLBACK: FAIL" >&2
  echo "ROLLED_BACK: true" >&2
  echo "REASON: validation command failed" >&2
  exit $validate_status
fi

echo "APPLY_WITH_ROLLBACK: PASS"
echo "ROLLED_BACK: false"
