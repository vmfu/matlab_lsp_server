#!/usr/bin/env python3
"""
LSP MATLAB Server - Release Package Creator

This script creates a distribution package for LSP MATLAB Server v0.1.0.
"""

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def create_release_package():
    """Create release package for distribution."""
    print("Creating LSP MATLAB Server v0.1.0 Release Package")

    # Define paths
    project_root = Path(__file__).parent
    release_dir = project_root / "dist" / "release"
    output_dir = project_root / "dist" / "packages"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Define package name
    version = "0.1.0"
    package_name = f"lsp_matlab_server_v{version}"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create .tar.gz package
    tar_file = output_dir / f"{package_name}_{timestamp}.tar.gz"

    print(f"\nCreating package: {tar_file.name}")

    try:
        # Create temporary directory for clean packaging
        temp_dir = output_dir / "temp_package"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()

        # Copy release files to temp directory
        # excluding .git, __pycache__, etc.
        print("Copying files...")

        # Copy all files and directories
        for item in release_dir.iterdir():
            if item.name.startswith("."):
                continue  # Skip hidden files
            if item.name == "__pycache__":
                continue  # Skip cache

            dest = temp_dir / item.name
            if item.is_dir():
                shutil.copytree(
                    item,
                    dest,
                    ignore=shutil.ignore_patterns(
                        ".git", "__pycache__", "*.pyc"
                    ),
                )
            else:
                shutil.copy2(item, dest)

        # Create tar.gz archive from temp directory
        print("Creating archive...")

        import tarfile

        with tarfile.open(tar_file, "w:gz") as tar:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.startswith("."):
                        continue  # Skip hidden files
                    if file.endswith(".pyc"):
                        continue  # Skip .pyc files

                    fullpath = os.path.join(root, file)
                    relpath = os.path.relpath(fullpath, temp_dir)
                    tar.add(fullpath, arcname=relpath)

        # Clean up temp directory
        shutil.rmtree(temp_dir)

        print(f"OK Package created: {tar_file}")
        file_size_kb = tar_file.stat().st_size / 1024
        print(f"  Size: {file_size_kb:.2f} KB")

        # Also create .zip for Windows users
        zip_file = output_dir / f"{package_name}_{timestamp}.zip"

        print(f"\nCreating package: {zip_file.name}")

        # Create .zip archive (requires Python 3.7+)
        if sys.version_info >= (3, 7):
            print("Creating archive...")

            import zipfile

            with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.startswith("."):
                            continue  # Skip hidden files
                        if file.endswith(".pyc"):
                            continue  # Skip .pyc files

                        fullpath = os.path.join(root, file)
                        relpath = os.path.relpath(fullpath, temp_dir)
                        zipf.write(fullpath, arcname=relpath)

            print(f"OK Package created: {zip_file}")
            file_size_kb = zip_file.stat().st_size / 1024
            print(f"  Size: {file_size_kb:.2f} KB")
        else:
            # Fallback for older Python versions
            print("  Skipping .zip (requires Python 3.7+)")

        # Create checksums
        print("\nCreating checksums...")

        if tar_file.exists():
            # MD5 checksum (for compatibility)
            import hashlib

            md5_hash = hashlib.md5()
            with open(tar_file, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    if not chunk:
                        break
                    md5_hash.update(chunk)
            md5_checksum = md5_hash.hexdigest()
            print(f"MD5 ({tar_file.name}): {md5_checksum}")

            # SHA256 checksum
            sha256_hash = hashlib.sha256()
            with open(tar_file, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    if not chunk:
                        break
                    sha256_hash.update(chunk)
            sha256_checksum = sha256_hash.hexdigest()
            print(f"SHA256 ({tar_file.name}): {sha256_checksum}")

        # Create checksum file
        checksum_file = (
            output_dir / f"{package_name}_{timestamp}.checksums.txt"
        )
        with open(checksum_file, "w") as f:
            f.write(f"LSP MATLAB Server v{version} - Checksums\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            if tar_file.exists():
                f.write(f"{tar_file.name}\n")
                f.write(f"MD5:    {md5_checksum}\n")
                f.write(f"SHA256: {sha256_checksum}\n\n")

            if zip_file.exists():
                # Also create checksums for .zip
                md5_zip = hashlib.md5()
                with open(zip_file, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        if not chunk:
                            break
                        md5_zip.update(chunk)
                f.write(f"{zip_file.name}\n")
                f.write(f"MD5:    {md5_zip.hexdigest()}\n")

        print(f"OK Checksums file: {checksum_file}")

        # Create release notes
        print("\nCreating release notes...")

        notes_file = (
            output_dir / f"{package_name}_{timestamp}.RELEASE_NOTES.txt"
        )
        with open(notes_file, "w") as f:
            f.write(f"LSP MATLAB Server v{version} - Release Notes\n")
            f.write("=" * 40 + "\n")
            f.write(f"Release Date: {datetime.now().strftime('%Y-%m-%d')}\n\n")

            f.write("Package Contents:\n")
            f.write("-" * 40 + "\n")
            f.write("Source Code (src/)\n")
            f.write("- MATLAB Parser\n")
            f.write("- LSP Handlers\n")
            f.write("- Utilities\n")
            f.write("- Analyzers\n")
            f.write("- Feature Management\n")
            f.write("- Protocol Implementation\n")
            f.write("-" * 40 + "\n")

            f.write("Documentation:\n")
            f.write("-" * 40 + "\n")
            f.write("- README.md (Installation Guide)\n")
            f.write("- INSTALL.md (Detailed Instructions)\n")
            f.write("- VERSION.md (Version Information)\n")
            f.write("- CHANGELOG.md (Version History)\n")
            f.write("- ARCHITECTURE.md (Design Documentation)\n")
            f.write("- DEVELOPMENT.md (Development Guide)\n")
            f.write("- TODO.md (Development Tasks - All Completed)\n")
            f.write("- RELEASE_NOTES.md (Release Notes)\n")
            f.write("-" * 40 + "\n")

            f.write("LSP Features:\n")
            f.write("-" * 40 + "\n")
            f.write("- textDocument/completion\n")
            f.write("- textDocument/hover\n")
            f.write("- textDocument/documentSymbol\n")
            f.write("- textDocument/definition\n")
            f.write("- textDocument/references\n")
            f.write("- textDocument/codeAction\n")
            f.write("- workspace/symbol\n")
            f.write("- textDocument/formatting\n")
            f.write("-" * 40 + "\n")

            f.write("Installation:\n")
            f.write("-" * 40 + "\n")
            f.write("1. Navigate to dist/release directory\n")
            f.write(
                "2. Install dependencies: pip install -r requirements.txt\n"
            )
            f.write("3. Run server: python run_server.py --stdio\n")
            f.write("-" * 40 + "\n")

            f.write("Requirements:\n")
            f.write("-" * 40 + "\n")
            f.write("- Python 3.10 or higher\n")
            f.write("- 4GB RAM recommended\n")
            f.write(
                "- Modern IDE with LSP support (VS Code 1.60+, "
                "JetBrains 2022+)\n"
            )
            f.write("-" * 40 + "\n")

            f.write("For detailed installation instructions, see INSTALL.md\n")
            f.write("=" * 40 + "\n")

        print(f"OK Release notes file: {notes_file}")

        # Summary
        print(f"\n{('=' * 60)}")
        print("Release Package Creation Summary")
        print("=" * 60)
        print(f"Version: {version}")
        print(f"Release Directory: {release_dir}")
        print(f"Output Directory: {output_dir}")
        print("\nPackages Created:")
        print(f"  1. {tar_file.name}")
        print(f"  2. {zip_file.name if zip_file.exists() else 'N/A'}")
        print("\nAdditional Files:")
        print(f"  1. {checksum_file.name}")
        print(f"  2. {notes_file.name}")
        tar_size = tar_file.stat().st_size
        zip_size = zip_file.stat().st_size if zip_file.exists() else 0
        total_mb = (tar_size + zip_size) / 1024 / 1024
        print(f"\nTotal Package Size: ~{total_mb:.2f} MB")
        print("=" * 60)

        print("\nOK Release package creation successful!")
        print(f"\nPackage files are located in: {output_dir}")

    except Exception as e:
        print(f"\nERROR Error creating release package: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    create_release_package()
