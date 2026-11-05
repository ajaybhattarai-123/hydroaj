"""
HydroAj Official PyPI Release Script
Safely prompts for your PyPI API token without PowerShell splitting/line-wrap issues.
"""
import getpass
import os
import sys
import subprocess

def main():
    print("=" * 70)
    print("   HydroAj v0.1.0 - Official PyPI Release Deployment")
    print("=" * 70)
    print("NOTE: Please ensure your token was generated at: https://pypi.org/manage/account/token/")
    print("      Scope MUST be: 'Entire account (all projects)' for this first release.")
    print("-" * 70)

    # Prompt securely without echoing and without PowerShell line-break splitting
    token = getpass.getpass("Paste your PyPI API token (starts with pypi-): ").strip()
    
    if not token.startswith("pypi-"):
        print("\n[ERROR] Invalid token format. PyPI tokens must start with 'pypi-'")
        sys.exit(1)

    # Check if this is a test.pypi.org token
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
    except Exception:
        repo_args = []

    print("\n[INFO] Authenticating and uploading distributions...")
    
    env = os.environ.copy()
    env["TWINE_USERNAME"] = "__token__"
    env["TWINE_PASSWORD"] = token

    cmd = [sys.executable, "-m", "twine", "upload", "--verbose"] + repo_args + [
        "target/wheels/hydroaj-0.1.0-cp311-cp311-win_amd64.whl",
        "target/wheels/hydroaj-0.1.0.tar.gz"
    ]

    ret = subprocess.call(cmd, env=env)
    if ret == 0:
        print("\n" + "=" * 70)
        print(" SUCCESS! HydroAj v0.1.0 is officially released!")
        print(" Anyone worldwide can now install it via: pip install hydroaj")
        print("=" * 70)
    else:
        print(f"\n[ERROR] Upload exited with code {ret}. See verbose logs above.")

if __name__ == "__main__":
    main()
