import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

def backup_file(path: Path) -> Path:
    ts = time.strftime("%Y%m%d-%H%M%S")
    bak = path.with_suffix(path.suffix + f".{ts}.bak")
    shutil.copy2(path, bak)
    return bak

def integrity_check_python(path: Path) -> (bool, str):
    import sqlite3
    try:
        with sqlite3.connect(str(path)) as conn:
            cur = conn.execute("PRAGMA integrity_check;")
            rows = [r[0] for r in cur.fetchall()]
            return (len(rows) == 1 and rows[0].lower() == 'ok', "\n".join(rows))
    except Exception as e:
        return (False, f"exception: {e}")

def run_sqlite_cli(cmd_args, input_text=None):
    try:
        proc = subprocess.run(cmd_args, input=input_text, text=True, capture_output=True)
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        return 127, "", "sqlite3 CLI not found in PATH"

def dump_with_cli(path: Path) -> (bool, str):
    code, out, err = run_sqlite_cli(["sqlite3", str(path), ".dump"]) 
    if code == 0 and out.strip():
        return True, out
    return False, err or out

def restore_dump_to_new_db(dump_sql: str, new_db: Path) -> bool:
    code, out, err = run_sqlite_cli(["sqlite3", str(new_db)], input_text=dump_sql)
    if code == 127:
        import sqlite3
        try:
            if new_db.exists():
                new_db.unlink()
            with sqlite3.connect(str(new_db)) as conn:
                conn.executescript(dump_sql)
            return True
        except Exception:
            return False
    else:
        return code == 0

def main():
    p = argparse.ArgumentParser(description="Inspect and attempt to recover a malformed SQLite DB")
    p.add_argument("db", nargs="?", default="assessment.db", help="Path to sqlite DB (default: assessment.db)")
    args = p.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"ERROR: DB file not found: {db_path}")
        sys.exit(2)

    print(f"Backing up {db_path}...")
    bak = backup_file(db_path)
    print(f"Backup created: {bak}")

    print("Running PRAGMA integrity_check via python sqlite3...")
    ok, result = integrity_check_python(db_path)
    print("Result:")
    print(result)
    if ok:
        print("Database reports OK. No further action required.")
        sys.exit(0)

    print("Integrity check failed or produced errors. Attempting to use sqlite3 CLI to dump...")
    success, dump_or_err = dump_with_cli(db_path)
    if success:
        dump_sql = dump_or_err
        print("Dump succeeded. Restoring dump into a new DB 'recovered.db'...")
        recovered = db_path.with_name(db_path.stem + "_recovered" + db_path.suffix)
        ok_restore = restore_dump_to_new_db(dump_sql, recovered)
        if ok_restore and recovered.exists():
            print(f"Recovered DB created: {recovered}")
            print("If recovered DB looks good, replace the original after manual verification.")
            sys.exit(0)
        else:
            print("Failed to restore dump into new DB.")
            print(dump_or_err)
            sys.exit(3)
    else:
        print("sqlite3 CLI dump failed or sqlite3 not found. Error / output:")
        print(dump_or_err)
        print("You can try these manual steps:")
        print("1) Install sqlite3 CLI from https://www.sqlite.org/download.html and ensure it's in PATH.")
        print("2) Run: sqlite3 <db> \"PRAGMA integrity_check;\" and sqlite3 <db> .dump > dump.sql")
        print("3) Create a new DB and import: sqlite3 recovered.db < dump.sql")
        sys.exit(4)

if __name__ == '__main__':
    main()
