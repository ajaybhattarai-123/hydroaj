"""
HydroAj Official PyPI Release Script
Smart and foolproof token reader with:
1. Auto-detection from Windows Clipboard
2. Visual masked confirmation so you see that it pasted
3. Secure upload via Twine
"""
import os
import sys
import subprocess

def get_clipboard_text():
    try:
        # Use PowerShell to safely read clipboard
        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
            capture_output=True,
            text=True,
            timeout=3
        )
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return ""

def main():
    print("=" * 72)
    print("   HydroAj v0.1.0 - Official PyPI Release Deployment")
    print("=" * 72)
    print("Requirement: Token from https://pypi.org/manage/account/token/")
    print("             Scope: 'Entire account (all projects)'")
    print("-" * 72)

    token = ""

    # Check 1: Auto-detect from clipboard
    clip = get_clipboard_text()
    # Remove any stray newlines or whitespace
    clean_clip = "".join(clip.split()) if clip else ""
    
    if clean_clip.startswith("pypi-"):
        print(f"\n[FOUND] Detected PyPI token in your clipboard!")
        masked = clean_clip[:15] + "..." + clean_clip[-10:]
        print(f"Token: {masked} ({len(clean_clip)} characters)")
        ans = input("Use this token from clipboard? (Y/n): ").strip().lower()
        if ans in ("", "y", "yes"):
            token = clean_clip

    # Check 2: If not in clipboard or rejected, ask for input with visible feedback
    if not token:
        print("\nPlease paste your token below and press Enter:")
        raw_input = input("Token: ").strip()
        token = "".join(raw_input.split())

    if not token.startswith("pypi-"):
        print("\n[ERROR] Invalid token format. A PyPI token must start with 'pypi-'")
        sys.exit(1)

    # Validate whether it is for production pypi.org vs test.pypi.org
    import base64
    try:
        raw = token[5:]
        padded = raw + '=' * (-len(raw) % 4)
        decoded = base64.urlsafe_b64decode(padded)
        if b'test.pypi.org' in decoded:
            print("\n[WARNING] This token belongs to TestPyPI (test.pypi.org), NOT production pypi.org!")
            print("To publish your real package so anyone can run 'pip install hydroaj',")
            print("please create a token at: https://pypi.org/manage/account/token/")
            choice = input("\nDo you still want to upload to TestPyPI instead of PyPI? (y/N): ").strip().lower()
            if choice == 'y':
                repo_args = ["--repository", "testpypi"]
            else:
                print("Cancelled. Please generate a production PyPI token and re-run.")
                sys.exit(0)
        else:
            repo_args = []
            print(f"\n[OK] Production PyPI token verified ({len(token)} characters).")
    except Exception:
        repo_args = []

    print("\n[INFO] Uploading release distributions to PyPI...")
    
    env = os.environ.copy()
    env["TWINE_USERNAME"] = "__token__"
    env["TWINE_PASSWORD"] = token

    cmd = [sys.executable, "-m", "twine", "upload", "--verbose"] + repo_args + [
        "target/wheels/hydroaj-0.1.0-cp311-cp311-win_amd64.whl",
        "target/wheels/hydroaj-0.1.0.tar.gz"
    ]

    ret = subprocess.call(cmd, env=env)
    if ret == 0:
        print("\n" + "=" * 72)
        print(" SUCCESS! HydroAj v0.1.0 is officially released on PyPI!")
        print(" Package page: https://pypi.org/project/hydroaj/")
        print(" Anyone worldwide can now run: pip install hydroaj")
        print("=" * 72)
    else:
        print(f"\n[ERROR] Upload exited with code {ret}. See verbose logs above.")

if __name__ == "__main__":
    main()
