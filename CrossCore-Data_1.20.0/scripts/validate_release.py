#!/usr/bin/env python3
from pathlib import Path
import argparse, gzip, hashlib, json

parser=argparse.ArgumentParser()
parser.add_argument("base", nargs="?", default="release_data")
parser.add_argument("--target", choices=("all","destiny","wargaming"), default="all")
args=parser.parse_args()
base=Path(args.base)

if args.target in {"all","destiny"}:
    m=json.loads((base/"destiny_data_manifest.json").read_text(encoding="utf-8"))
    payload=(base/"destiny_items.json.gz").read_bytes()
    assert hashlib.sha256(payload).hexdigest()==m["sha256"]
    data=json.loads(gzip.decompress(payload).decode("utf-8"))
    assert len(data["items"])==m["item_count"]
    assert data["manifest_version"]==m["manifest_version"]

if args.target in {"all","wargaming"}:
    m=json.loads((base/"wargaming_data_manifest.json").read_text(encoding="utf-8"))
    for game in ("wot","wows"):
        payload=(base/f"{game}_catalog.json.gz").read_bytes()
        assert hashlib.sha256(payload).hexdigest()==m[game]["sha256"]
        data=json.loads(gzip.decompress(payload).decode("utf-8"))
        assert data["game"]==game
        assert len(data["items"])==m[game]["item_count"]
print("Alle angeforderten Release-Dateien sind gültig.")
