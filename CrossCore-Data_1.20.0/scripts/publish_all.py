#!/usr/bin/env python3
"""Erzeugt alle öffentlichen CrossCore-Datendateien."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OUT = Path("release_data")
RELEASE_BASE = "https://github.com/unhappyangel83/CrossCore-Data/releases/download/data-latest"


def request_json(url: str, params=None, headers=None, timeout=180):
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def request_bytes(url: str, headers=None, timeout=240) -> bytes:
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=timeout) as response:
        return response.read()


def publish_destiny() -> dict:
    key = os.environ.get("BUNGIE_API_KEY", "").strip()
    if not key:
        raise RuntimeError("BUNGIE_API_KEY fehlt.")

    headers = {
        "X-API-Key": key,
        "Accept": "application/json",
        "User-Agent": "CrossCore-Data GitHub Publisher",
    }
    manifest = request_json(
        "https://www.bungie.net/Platform/Destiny2/Manifest/",
        headers=headers,
        timeout=60,
    )
    response = manifest.get("Response") or {}
    paths = response.get("jsonWorldComponentContentPaths") or {}
    de_path = (paths.get("de") or {}).get("DestinyInventoryItemDefinition")
    en_path = (paths.get("en") or {}).get("DestinyInventoryItemDefinition")
    if not de_path or not en_path:
        raise RuntimeError("DestinyInventoryItemDefinition fehlt.")

    def absolute(path):
        return path if path.startswith("http") else "https://www.bungie.net" + path

    de_items = request_json(absolute(de_path), headers=headers, timeout=300)
    en_items = request_json(absolute(en_path), headers=headers, timeout=300)

    items = []
    for item_hash in sorted(set(de_items) | set(en_items), key=lambda x: int(x)):
        de = de_items.get(item_hash) or {}
        en = en_items.get(item_hash) or {}
        de_display = de.get("displayProperties") or {}
        en_display = en.get("displayProperties") or {}
        name_de = str(de_display.get("name") or en_display.get("name") or "").strip()
        name_en = str(en_display.get("name") or name_de).strip()
        if not name_de and not name_en:
            continue
        inventory = de.get("inventory") or en.get("inventory") or {}
        source_data = de.get("sourceData") or en.get("sourceData") or {}
        sockets = de.get("sockets") or en.get("sockets") or {}
        items.append({
            "hash": str(item_hash),
            "name_de": name_de or name_en,
            "name_en": name_en or name_de,
            "description_de": str(de_display.get("description") or ""),
            "description_en": str(en_display.get("description") or ""),
            "type_de": str(de.get("itemTypeDisplayName") or ""),
            "type_en": str(en.get("itemTypeDisplayName") or ""),
            "tier": str(inventory.get("tierTypeName") or ""),
            "item_type": de.get("itemType", en.get("itemType")),
            "item_sub_type": de.get("itemSubType", en.get("itemSubType")),
            "class_type": de.get("classType", en.get("classType")),
            "equippable": bool(de.get("equippable", en.get("equippable", False))),
            "collectible_hash": de.get("collectibleHash", en.get("collectibleHash")),
            "icon": str(de_display.get("icon") or en_display.get("icon") or ""),
            "screenshot": str(de.get("screenshot") or en.get("screenshot") or ""),
            "socket_count": len(sockets.get("socketEntries") or []),
            "source_category": source_data.get("sourceCategory"),
            "source_hashes": source_data.get("sourceHashes") or [],
            "lightgg_url": f"https://www.light.gg/db/items/{item_hash}/",
            "destinysets_url": "https://data.destinysets.com/i/InventoryItem%3A" + str(item_hash),
        })

    cache = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "manifest_version": str(response.get("version") or ""),
        "source": "https://www.bungie.net/Platform/Destiny2/Manifest/",
        "items": sorted(items, key=lambda x: (x["name_de"].casefold(), x["hash"])),
    }
    plain = json.dumps(cache, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    compressed = gzip.compress(plain, compresslevel=9, mtime=0)
    path = OUT / "destiny_items.json.gz"
    path.write_bytes(compressed)
    digest = hashlib.sha256(compressed).hexdigest()
    result = {
        "schema_version": 1,
        "manifest_version": cache["manifest_version"],
        "generated_at": cache["updated_at"],
        "item_count": len(cache["items"]),
        "compressed_size": len(compressed),
        "uncompressed_size": len(plain),
        "sha256": digest,
        "data_url": RELEASE_BASE + "/destiny_items.json.gz",
        "source": "Bungie Destiny Manifest",
    }
    (OUT / "destiny_data_manifest.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result


def wg_pages(url: str, app_id: str, language: str) -> list[dict]:
    page = 1
    result = []
    while True:
        payload = request_json(url, {
            "application_id": app_id,
            "language": language,
            "limit": 100,
            "page_no": page,
        }, timeout=120)
        if payload.get("status") != "ok":
            raise RuntimeError(str(payload.get("error")))
        result.extend((payload.get("data") or {}).values())
        meta = payload.get("meta") or {}
        if page >= int(meta.get("page_total", page)):
            return result
        page += 1
        time.sleep(0.15)


def normalize_wg(game: str, de_rows: list[dict], en_rows: list[dict], source_url: str):
    id_field = "tank_id" if game == "wot" else "ship_id"
    en_map = {str(row.get(id_field)): row for row in en_rows}
    items = []
    for row in de_rows:
        ident = str(row.get(id_field))
        en = en_map.get(ident, {})
        images = row.get("images") or {}
        profile = row.get("default_profile") or {}
        mobility = profile.get("mobility") or {}
        survivability = profile.get("survivability") or {}
        items.append({
            "id": ident,
            "name_de": row.get("name", ""),
            "name_en": en.get("name", row.get("name", "")),
            "type": row.get("type", ""),
            "nation": row.get("nation", ""),
            "tier": row.get("tier", 0),
            "premium": bool(row.get("is_premium", False)),
            "hp": survivability.get("health", profile.get("hp", "—")),
            "speed": mobility.get("max_speed", row.get("speed_forward", "—")),
            "damage": "—",
            "range": "—",
            "description": row.get("description", ""),
            "image": images.get("big") or images.get("large") or images.get("small") or "",
            "official_url": "",
            "source_url": source_url,
            "source_name": "Offizielle Wargaming API",
        })
    return sorted(items, key=lambda item: (str(item["name_de"]).casefold(), str(item["id"])))


def publish_wargaming() -> dict:
    app_id = os.environ.get("WARGAMING_APPLICATION_ID", "").strip()
    if not app_id:
        raise RuntimeError("WARGAMING_APPLICATION_ID fehlt.")

    generated = datetime.now(timezone.utc).isoformat()
    result = {"schema_version": 1, "generated_at": generated}
    endpoints = {
        "wot": "https://api.worldoftanks.eu/wot/encyclopedia/vehicles/",
        "wows": "https://api.worldofwarships.eu/wows/encyclopedia/ships/",
    }
    for game, url in endpoints.items():
        de = wg_pages(url, app_id, "de")
        en = wg_pages(url, app_id, "en")
        items = normalize_wg(game, de, en, url)
        catalog = {"game": game, "updated_at": generated, "source": [url], "items": items}
        plain = json.dumps(catalog, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        compressed = gzip.compress(plain, compresslevel=9, mtime=0)
        filename = f"{game}_catalog.json.gz"
        (OUT / filename).write_bytes(compressed)
        result[game] = {
            "version": generated,
            "item_count": len(items),
            "compressed_size": len(compressed),
            "uncompressed_size": len(plain),
            "sha256": hashlib.sha256(compressed).hexdigest(),
            "data_url": RELEASE_BASE + "/" + filename,
            "source": url,
        }
    (OUT / "wargaming_data_manifest.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=("all", "destiny", "wargaming"), default="all")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    result = {}
    if args.target in {"all", "destiny"}:
        result["destiny"] = publish_destiny()
    if args.target in {"all", "wargaming"}:
        result["wargaming"] = publish_wargaming()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
