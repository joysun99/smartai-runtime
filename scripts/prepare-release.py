#!/usr/bin/env python3
"""Verify pinned smartai runtime archives and stage GitHub Release metadata.

Archives stay at their source paths; this script does not upload or copy them.
"""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
import tempfile
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = "c3e12e4654092cb0b9b54a2fb89b947753111a37facfe6754a8c0538234efdc1"
REPOSITORY = "joysun99/smartai-runtime"


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_member(source):
    digest = hashlib.sha256()
    length = 0
    for chunk in iter(lambda: source.read(1024 * 1024), b""):
        digest.update(chunk)
        length += len(chunk)
    return length, digest.hexdigest()


def safe_member(name):
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts and str(path) == name and "\\" not in name


def inspect_archive(path, record):
    if path.stat().st_size != record["archive_bytes"] or sha256_file(path) != record["archive_sha256"]:
        raise ValueError(f"archive identity mismatch: {record['id']}")
    observed = {}
    manifest_bytes = None
    with tarfile.open(path, "r:gz") as archive:
        for member in archive:
            name = member.name
            if not safe_member(name) or name in observed:
                raise ValueError(f"unsafe or duplicate member: {name}")
            if member.isfile():
                if name == "runtime.json":
                    manifest_bytes = archive.extractfile(member).read()
                    observed[name] = {"type": "file", "bytes": len(manifest_bytes),
                                      "sha256": hashlib.sha256(manifest_bytes).hexdigest()}
                else:
                    length, digest = sha256_member(archive.extractfile(member))
                    observed[name] = {"type": "file", "bytes": length, "sha256": digest}
            elif member.issym():
                target = member.linkname
                if not target or target in (".", "..") or "/" in target or "\\" in target:
                    raise ValueError(f"unsafe symlink: {name}")
                observed[name] = {"type": "symlink", "target": target}
            else:
                raise ValueError(f"unsupported archive member: {name}")
    if not manifest_bytes or hashlib.sha256(manifest_bytes).hexdigest() != record["manifest_sha256"]:
        raise ValueError(f"manifest identity mismatch: {record['id']}")
    manifest = json.loads(manifest_bytes)
    for key in ("id", "service", "backend"):
        if manifest.get(key) != record[key]:
            raise ValueError(f"manifest {key} mismatch: {record['id']}")
    expected = {item["path"]: item for item in manifest["files"]}
    if len(expected) != len(manifest["files"]) or set(observed) != set(expected) | {"runtime.json"}:
        raise ValueError(f"archive inventory mismatch: {record['id']}")
    for name, item in expected.items():
        actual = observed[name]
        for key in (("type", "bytes", "sha256") if item["type"] == "file" else ("type", "target")):
            if item[key] != actual[key]:
                raise ValueError(f"payload identity mismatch: {record['id']}:{name}:{key}")
    licenses = sorted(name for name in expected if name.startswith("licenses/") and expected[name]["type"] == "file")
    if record["service"] != "otelcol" and not licenses:
        raise ValueError(f"missing bundled license inventory: {record['id']}")
    unpacked = sum(item["bytes"] for item in observed.values() if item["type"] == "file")
    return manifest, licenses, unpacked


def write_json(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare(args):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.tag):
        raise ValueError("invalid release tag")
    if args.output.exists() or args.output.is_symlink():
        raise ValueError(f"output already exists: {args.output}")
    source_catalog = ROOT / "source-catalog.json"
    if sha256_file(source_catalog) != SOURCE_SHA256:
        raise ValueError("source catalog changed; pin a new source identity")
    records = json.loads(source_catalog.read_text(encoding="utf-8"))["runtimes"]
    if len(records) != 8 or len({record["id"] for record in records}) != len(records):
        raise ValueError("candidate count or identity changed")
    if len({record["archive"] for record in records}) != len(records):
        raise ValueError("duplicate archive name")
    base_url = f"https://github.com/{REPOSITORY}/releases/download/{quote(args.tag)}"
    entries, recommendations, inventory, sources = [], [], [], []
    for record in sorted(records, key=lambda item: item["id"]):
        name = record["archive"]
        if Path(name).name != name or not name.endswith(".tar.gz"):
            raise ValueError(f"unsafe archive name: {name}")
        directory = (args.cuda_dir if record["backend"] == "cuda" else
                     args.collector_dir if record["service"] == "otelcol" else
                     args.tts_dir if record["service"] == "kokoro" else args.m0_dir)
        path = directory / name
        manifest, licenses, unpacked = inspect_archive(path, record)
        entry = {key: record[key] for key in ("id", "service", "backend", "archive_bytes", "archive_sha256", "manifest_sha256")}
        entry.update(platform=manifest["platform"], version=manifest["version"],
                     archive_url=f"{base_url}/{quote(name)}", unpacked_bytes=unpacked)
        entries.append(entry)
        recommendations.append({key: entry[key] for key in ("service", "platform", "backend", "id")})
        inventory.append({"id": record["id"], "archive": name, "license_files": licenses,
                          "license_review": "pending", "minimum_glibc_symbol_version": record.get("minimum_glibc_symbol_version"),
                          "external_libraries": record.get("external_libraries", {})})
        sources.append({"archive": name, "path": str(path.resolve())})
    if len({(item["service"], item["platform"], item["backend"]) for item in recommendations}) != len(entries):
        raise ValueError("ambiguous recommendations")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".prepare-", dir=args.output.parent) as temporary:
        stage = Path(temporary)
        write_json(stage / "catalog.json", {"schema_version": 2, "runtimes": entries, "recommendations": recommendations})
        write_json(stage / "release-inventory.json", {"schema_version": 1,
                   "source_catalog_sha256": SOURCE_SHA256, "release_tag": args.tag,
                   "license_review": "pending", "runtimes": inventory})
        write_json(stage / "upload-sources.json", {"schema_version": 1, "sources": sources})
        sums = [(record["archive_sha256"], record["archive"]) for record in records]
        sums.extend((sha256_file(stage / name), name) for name in ("catalog.json", "release-inventory.json"))
        (stage / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for digest, name in sorted(sums, key=lambda item: item[1])), encoding="utf-8")
        stage.rename(args.output)
    return entries


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--m0-dir", type=Path, required=True)
    parser.add_argument("--tts-dir", type=Path, required=True)
    parser.add_argument("--cuda-dir", type=Path, required=True)
    parser.add_argument("--collector-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        result = prepare(arguments)
    except (OSError, KeyError, ValueError, tarfile.TarError) as error:
        parser.exit(1, f"error: {error}\n")
    print(json.dumps({"output": str(arguments.output), "candidates": len(result),
                      "archive_bytes": sum(item["archive_bytes"] for item in result),
                      "license_review": "pending", "published": False}, ensure_ascii=False))
