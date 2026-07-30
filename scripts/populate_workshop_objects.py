#!/usr/bin/env python3
"""Populate workshop metadata CSV and capture homepage screenshots.

Draft content for Warp and Weft workshop collection objects.
Run from repo root: python3 scripts/populate_workshop_objects.py
"""
from __future__ import annotations

import csv
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOT_DIR = ROOT / "objects" / "screenshots"
SMALL_DIR = ROOT / "objects" / "small"
THUMB_DIR = ROOT / "objects" / "thumbs"
META_PATH = ROOT / "_data" / "workshop-metadata.csv"

SHOT_DIR.mkdir(parents=True, exist_ok=True)
SMALL_DIR.mkdir(parents=True, exist_ok=True)
THUMB_DIR.mkdir(parents=True, exist_ok=True)

# Two kinds of objects:
# - digital project: homepage screenshot + link (display_template=image)
# - citation: article/book record with URL (display_template=record)
ITEMS = [
    # --- digital projects ---
    {
        "objectid": "digital_benin",
        "kind": "project",
        "title": "Digital Benin",
        "creator": "Digital Benin",
        "date": "2022",
        "url": "https://digitalbenin.org/",
        "screenshot_url": "https://digitalbenin.org/",
        "description": (
            "Community-centered knowledge production about stolen cultural heritage, "
            "using multiple forms and presentations of knowledge and local-language "
            "metadata terminology (oral history, storytelling, critical reflections "
            "on metadata and archiving). Recommended by Reina Gattuso."
        ),
        "subject": "digital project; digital archive; community archive; cultural heritage restitution; Indigenous knowledge; multilingual metadata",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "Reina Gattuso",
        "image_alt_text": "Screenshot of the Digital Benin homepage",
    },
    {
        "objectid": "whose_knowledge",
        "kind": "project",
        "title": "Whose Knowledge?",
        "creator": "Whose Knowledge?",
        "date": "",
        "url": "https://whoseknowledge.org/",
        # Site returns 403 to headless browsers; keep as link-only record for now.
        "screenshot_url": None,
        "description": (
            "A global campaign to center the knowledge of marginalized communities "
            "on the internet. Recommended by Garrett Graddy-Lovelace."
        ),
        "subject": "digital project; knowledge justice; community archive; digital equity",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "Garrett Graddy-Lovelace",
        "image_alt_text": "Screenshot of the Whose Knowledge? homepage",
    },
    {
        "objectid": "mukurtu",
        "kind": "project",
        "title": "Mukurtu CMS",
        "creator": "Mukurtu / Center for Digital Scholarship and Curation, Washington State University",
        "date": "",
        "url": "https://mukurtu.org/",
        "screenshot_url": "https://mukurtu.org/",
        "description": (
            "A content management system designed for Indigenous collections, "
            "supporting community protocols for access and description. "
            "Recommended by Sharon Mizota."
        ),
        "subject": "digital project; CMS; Indigenous collections; Indigenous data sovereignty; digital archive",
        "type": "Software",
        "format": "text/html",
        "recommended_by": "Sharon Mizota",
        "image_alt_text": "Screenshot of the Mukurtu CMS homepage",
    },
    {
        "objectid": "whose_knowledge_dti",
        "kind": "project",
        "title": "Whose Knowledge? — Decolonizing the Internet’s Structured Data Report",
        "creator": "Whose Knowledge?",
        "date": "",
        "url": "https://whoseknowledge.org/resource/dti-structured-data-report/",
        # Site returns 403 to headless browsers; keep as link-only record for now.
        "screenshot_url": None,
        "description": (
            "Report and resource on decolonizing structured data on the internet, "
            "from Whose Knowledge?."
        ),
        "subject": "digital project; report; structured data; knowledge justice; metadata",
        "type": "Text",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the Whose Knowledge? DTI Structured Data Report page",
    },
    {
        "objectid": "niiwin",
        "kind": "project",
        "title": "Niiwin",
        "creator": "Niiwin",
        "date": "",
        "url": "https://niiwin.app/",
        "screenshot_url": "https://niiwin.app/",
        "description": "Indigenous data sovereignty software.",
        "subject": "digital project; Indigenous data sovereignty; software; metadata tool",
        "type": "Software",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the Niiwin app homepage",
    },
    {
        "objectid": "rrn",
        "kind": "project",
        "title": "Reciprocal Research Network (RRN)",
        "creator": "Musqueam Indian Band; Stó:lō Nation/Tribal Council; U’mista Cultural Society; Museum of Anthropology at UBC",
        "date": "",
        "url": "https://www.rrncommunity.org/",
        "screenshot_url": "https://www.rrncommunity.org/",
        "description": (
            "A collaborative online research tool for Northwest Coast First Nations "
            "cultural heritage held across partner institutions. Supports reciprocal "
            "research between communities, researchers, and museums."
        ),
        "subject": "digital project; digital archive; Indigenous collections; reciprocal research; community archive",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the Reciprocal Research Network homepage",
    },
    {
        "objectid": "design_justice",
        "kind": "project",
        "title": "Design Justice (MIT Press open access book)",
        "creator": "Costanza-Chock, Sasha / Design Justice Network",
        "date": "2020",
        "url": "https://designjustice.mitpress.mit.edu/",
        "screenshot_url": "https://designjustice.mitpress.mit.edu/",
        "description": (
            "Open-access book on design justice for digital tools and systems. "
            "A touchstone for thinking about who design processes center and exclude."
        ),
        "subject": "digital project; design justice; open access book; digital tools",
        "type": "Text",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the Design Justice open-access book site",
    },
    {
        "objectid": "calisphere",
        "kind": "project",
        "title": "Calisphere",
        "creator": "California Digital Library / University of California",
        "date": "",
        "url": "https://calisphere.org/overview/",
        # Homepage screenshot capture currently fails in headless Chrome; record for now.
        "screenshot_url": None,
        "description": (
            "A repository aggregating resources from many memory organizations in "
            "California, with substantial documentation of process and practice."
        ),
        "subject": "digital project; digital archive; repository aggregator; memory institutions",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the Calisphere overview page",
    },
    {
        "objectid": "rikolti",
        "kind": "project",
        "title": "Rikolti (Calisphere 2.0 harvester)",
        "creator": "University of California Libraries Digital Collection (ucldc)",
        "date": "",
        "url": "https://github.com/ucldc/rikolti",
        "screenshot_url": "https://github.com/ucldc/rikolti",
        "description": (
            "Open-source harvester powering Calisphere 2.0 metadata aggregation "
            "across contributing institutions."
        ),
        "subject": "digital project; metadata tool; harvester; repository aggregator; open source",
        "type": "Software",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the Rikolti GitHub repository",
    },
    {
        "objectid": "sssom",
        "kind": "project",
        "title": "SSSOM — Simple Standard for Sharing Ontological Mappings",
        "creator": "Mapping Commons / SSSOM community",
        "date": "",
        "url": "https://mapping-commons.github.io/sssom/",
        "screenshot_url": "https://mapping-commons.github.io/sssom/",
        "description": (
            "A community-driven standard designed to facilitate the exchange and "
            "integration of semantic entity mappings. Encountered via Digital "
            "Scriptorium's work on inter-relating data mappings."
        ),
        "subject": "digital project; ontology; metadata standard; semantic mapping; controlled vocabulary",
        "type": "Text",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the SSSOM documentation site",
    },
    {
        "objectid": "yamz",
        "kind": "project",
        "title": "YAMZ",
        "creator": "YAMZ",
        "date": "",
        "url": "https://yamz.net/",
        "screenshot_url": "https://yamz.net/",
        "description": (
            'YAMZ (pronounced "yams") is an open vocabulary of metadata terms from '
            'all domains and from all parts of "metadata speech."'
        ),
        "subject": "digital project; metadata tool; controlled vocabulary; open vocabulary",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the YAMZ homepage",
    },
    {
        "objectid": "black_publishing",
        "kind": "project",
        "title": "Black Self-Publishing — Methodology (American Antiquarian Society)",
        "creator": "American Antiquarian Society",
        "date": "",
        "url": "https://collections.americanantiquarian.org/blackpublishing/methodology",
        "screenshot_url": "https://collections.americanantiquarian.org/blackpublishing/methodology",
        "description": (
            "Methodology writing on how the project determined keywords, searching, "
            "and decisions about inclusion in a digital collection of Black self-publishing."
        ),
        "subject": "digital project; digital archive; methodology; keywording; Black publishing",
        "type": "Text",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the Black Self-Publishing methodology page",
    },
    {
        "objectid": "digital_scriptorium",
        "kind": "project",
        "title": "Digital Scriptorium — About / Data Model",
        "creator": "Digital Scriptorium",
        "date": "",
        "url": "https://digital-scriptorium.org/about/about-ds/",
        "screenshot_url": "https://digital-scriptorium.org/about/about-ds/",
        "description": (
            "Documentation of Digital Scriptorium's data model and how it brings "
            "together metadata from various repositories and layers it."
        ),
        "subject": "digital project; digital archive; data model; metadata aggregation; manuscripts",
        "type": "Text",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the Digital Scriptorium About page",
    },
    {
        "objectid": "gender_network",
        "kind": "project",
        "title": "gender.network",
        "creator": "gender.network",
        "date": "",
        "url": "https://gender.network/about",
        "screenshot_url": "https://gender.network/about",
        "description": (
            "A manually aggregated archive of trans zine culture."
        ),
        "subject": "digital project; community archive; queer archives; zines; manual aggregation",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the gender.network about page",
    },
    {
        "objectid": "on_these_grounds",
        "kind": "project",
        "title": "On These Grounds — Descriptive Model",
        "creator": "On These Grounds",
        "date": "",
        "url": "https://onthesegrounds.org/s/OTG/page/descriptive-model",
        "screenshot_url": "https://onthesegrounds.org/s/OTG/page/descriptive-model",
        "description": (
            "Data model, descriptive model, and controlled vocabularies framed "
            "theoretically, with writing about implementing the model in Omeka S. "
            "A touchstone for making sense of controlled vocabularies mid-project. "
            "Aims to create, evaluate, revise, and disseminate a LOD ontology focused "
            "on adequately describing the lived experiences of enslaved individuals "
            "who labored in bondage at higher education institutions; create resources "
            "enabling other colleges and universities to undertake this work; and "
            "aggregate resulting data to increase discoverability and foster new scholarship."
        ),
        "subject": "digital project; LOD ontology; controlled vocabulary; data model; Omeka S; slavery studies; higher education archives",
        "type": "Text",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the On These Grounds descriptive model page",
    },
    {
        "objectid": "rhizome_object",
        "kind": "project",
        "title": "Rhizome — archived public art / VR-related object",
        "creator": "Rhizome",
        "date": "2010",
        "url": "https://web.archive.org/web/20100429114826/http://rhizome.org/object.php?49840",
        # Wayback captures often fail to screenshot reliably; record for now.
        "screenshot_url": None,
        "description": (
            "Archived Rhizome object page (web.archive.org capture). Cited as a "
            "touchstone for Sara alongside e-artexte and Flourish when going into "
            "the project."
        ),
        "subject": "digital project; new media archive; web archive; public art; VR",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "Sara",
        "image_alt_text": "Screenshot of an archived Rhizome object page",
    },
    {
        "objectid": "blackity",
        "kind": "project",
        "title": "Blackity (Artexte)",
        "creator": "Artexte",
        "date": "",
        "url": "https://www.artexte.art/en/blackity",
        "screenshot_url": "https://www.artexte.art/en/blackity",
        "description": (
            "Artexte project Blackity. A touchstone for Sara going into the project, "
            "alongside Rhizome and Flourish."
        ),
        "subject": "digital project; digital archive; art documentation; Black art",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "Sara",
        "image_alt_text": "Screenshot of the Blackity project page on Artexte",
    },
    {
        "objectid": "e_artexte",
        "kind": "project",
        "title": "e-artexte",
        "creator": "Artexte",
        "date": "",
        "url": "https://e-artexte.ca/information.html",
        "screenshot_url": "https://e-artexte.ca/information.html",
        "description": (
            "e-artexte information / digital repository documentation. A touchstone "
            "for Sara going into the project."
        ),
        "subject": "digital project; digital archive; art documentation; repository",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "Sara",
        "image_alt_text": "Screenshot of the e-artexte information page",
    },
    {
        "objectid": "flourish",
        "kind": "project",
        "title": "Flourish — data visualization examples",
        "creator": "Flourish",
        "date": "",
        "url": "https://flourish.studio/examples/",
        "screenshot_url": "https://flourish.studio/examples/",
        "description": (
            "Data visualization example gallery. Cited as a touchstone for Sara "
            "alongside Rhizome and e-artexte."
        ),
        "subject": "digital project; data visualization; digital tools",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "Sara",
        "image_alt_text": "Screenshot of the Flourish examples gallery",
    },
    {
        "objectid": "gent_gemapt",
        "kind": "project",
        "title": "Gent Gemapt (kaart.gentgemapt.be)",
        "creator": "Gent Gemapt",
        "date": "",
        "url": "https://kaart.gentgemapt.be/",
        "screenshot_url": "https://kaart.gentgemapt.be/",
        "description": (
            "A site that uses both a timeline and a map as navigation tools over "
            "a digital collection."
        ),
        "subject": "digital project; digital archive; map; timeline; collection navigation",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the Gent Gemapt map/timeline interface",
    },
    {
        "objectid": "printed_matter",
        "kind": "project",
        "title": "Printed Matter — catalog item (data model reference)",
        "creator": "Printed Matter, Inc.",
        "date": "",
        "url": "https://www.printedmatter.org/catalog/71513",
        "screenshot_url": "https://www.printedmatter.org/catalog/71513",
        "description": (
            "Example catalog record illustrating Printed Matter's data model and "
            "visually impactful website design for artists' books and publications."
        ),
        "subject": "digital project; publisher catalog; data model; artists books",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of a Printed Matter catalog record page",
    },
    {
        "objectid": "fire_lines",
        "kind": "project",
        "title": "Fire Lines",
        "creator": "Center for Digital Inquiry and Learning (CDIL), University of Idaho",
        "date": "",
        "url": "https://cdil.lib.uidaho.edu/fire-lines/",
        "screenshot_url": "https://cdil.lib.uidaho.edu/fire-lines/",
        "description": (
            "CollectionBuilder digital collection / exhibit with a colorful, "
            "impactful visual design. Useful reference for CollectionBuilder-based "
            "publishing."
        ),
        "subject": "digital project; digital archive; CollectionBuilder; exhibit",
        "type": "InteractiveResource",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "Screenshot of the Fire Lines CollectionBuilder site",
    },
    # --- citations ---
    {
        "objectid": "cite_paradata_mizota",
        "kind": "citation",
        "title": "Paradata: data about how the data was collected",
        "creator": "Mizota, Sharon",
        "date": "2023",
        "url": "https://www.curationist.org/editorial-features/article/metadata-learning-and-unlearning-summit-2023",
        "screenshot_url": None,
        "description": (
            "Concept of paradata (data about how data was collected) highlighted by "
            "Sharon Mizota in the context of the Metadata Learning and Unlearning "
            "Summit 2023 (Curationist). Emphasizes documenting collection processes "
            "so users can understand perspective, bias, and uncertainty in metadata."
        ),
        "subject": "citation; paradata; metadata methodology; knowledge justice",
        "type": "Text",
        "format": "text/html",
        "recommended_by": "Sharon Mizota",
        "image_alt_text": "",
    },
    {
        "objectid": "cite_rrn_reflection",
        "kind": "citation",
        "title": "Reflections on the Reciprocal Research Network",
        "creator": "",
        "date": "",
        "url": "https://scholarworks.iu.edu/journals/index.php/mar/article/view/2172",
        "screenshot_url": None,
        "description": (
            "Scholarly article reflecting on the Reciprocal Research Network (RRN), "
            "companion reading to the RRN digital project object."
        ),
        "subject": "citation; reciprocal research; Indigenous collections; digital archive; scholarly article",
        "type": "Text",
        "format": "text/html",
        "recommended_by": "",
        "image_alt_text": "",
    },
]

COLUMNS = [
    "objectid",
    "parentid",
    "title",
    "creator",
    "date",
    "date-is-approximate?",
    "description",
    "subject",
    "location",
    "latitude",
    "longitude",
    "source",
    "identifier",
    "type",
    "format",
    "language",
    "rights",
    "rightsstatement",
    "display_template",
    "object_location",
    "image_small",
    "image_thumb",
    "image_alt_text",
    "object_transcript",
]


def capture_screenshot(url: str, out_path: Path) -> bool:
    """Capture a viewport screenshot with headless Chrome.

    Chrome often writes the screenshot then hangs instead of exiting cleanly
    in this environment, so we poll for the file and kill the process once
    a usable image appears.
    """
    import shutil
    import tempfile

    tmp = out_path.with_suffix(".tmp.png")
    tmp.unlink(missing_ok=True)
    profile = tempfile.mkdtemp(prefix="chrome-shot-")
    cmd = [
        "google-chrome",
        "--headless=new",
        "--single-process",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--hide-scrollbars",
        "--remote-debugging-port=0",
        f"--user-data-dir={profile}",
        f"--screenshot={tmp}",
        "--window-size=1400,900",
        url,
    ]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 75
        stable_hits = 0
        last_size = -1
        while time.time() < deadline:
            if tmp.exists():
                size = tmp.stat().st_size
                if size > 8000:
                    if size == last_size:
                        stable_hits += 1
                    else:
                        stable_hits = 0
                        last_size = size
                    if stable_hits >= 2:
                        break
            if proc.poll() is not None:
                break
            time.sleep(0.5)

        if proc.poll() is None:
            proc.kill()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

        if tmp.exists() and tmp.stat().st_size > 8000:
            subprocess.run(
                ["convert", str(tmp), "-quality", "85", str(out_path)],
                check=False,
                capture_output=True,
            )
            tmp.unlink(missing_ok=True)
            ok = out_path.exists() and out_path.stat().st_size > 2000
            return ok
        print(f"  WARN: no usable screenshot for {url}", flush=True)
        tmp.unlink(missing_ok=True)
        return False
    except Exception as exc:  # noqa: BLE001
        print(f"  ERROR capturing {url}: {exc}", flush=True)
        if proc.poll() is None:
            proc.kill()
        tmp.unlink(missing_ok=True)
        return False
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def make_derivatives(full_path: Path, objectid: str) -> tuple[str, str]:
    small = SMALL_DIR / f"{objectid}_sm.jpg"
    thumb = THUMB_DIR / f"{objectid}_th.jpg"
    # CollectionBuilder defaults: small ~800px, thumb ~400px (approx)
    subprocess.run(
        ["convert", str(full_path), "-resize", "800x>", "-quality", "82", str(small)],
        check=False,
        capture_output=True,
    )
    subprocess.run(
        ["convert", str(full_path), "-resize", "400x>", "-quality", "80", str(thumb)],
        check=False,
        capture_output=True,
    )
    return f"/objects/small/{small.name}", f"/objects/thumbs/{thumb.name}"


def build_row(item: dict, has_shot: bool) -> dict:
    row = {c: "" for c in COLUMNS}
    row["objectid"] = item["objectid"]
    row["title"] = item["title"]
    row["creator"] = item["creator"]
    row["date"] = item["date"]
    row["description"] = item["description"]
    row["subject"] = item["subject"]
    row["source"] = item["url"]
    row["identifier"] = item["url"]
    row["type"] = item["type"]
    row["format"] = item["format"]
    row["language"] = "eng"
    row["rights"] = "Refer to source site for rights; screenshots used for educational workshop reference."
    row["image_alt_text"] = item.get("image_alt_text", "")

    if item["kind"] == "project" and has_shot:
        shot_rel = f"/objects/screenshots/{item['objectid']}.jpg"
        row["display_template"] = "image"
        row["object_location"] = shot_rel
        small, thumb = make_derivatives(SHOT_DIR / f"{item['objectid']}.jpg", item["objectid"])
        row["image_small"] = small
        row["image_thumb"] = thumb
    elif item["kind"] == "project":
        # Screenshot failed — still linkable image-less project as a record
        row["display_template"] = "record"
        row["object_location"] = item["url"]
        row["format"] = "text/html"
    else:
        row["display_template"] = "record"
        row["object_location"] = item["url"]
    return row


def seed_known_screenshots() -> None:
    """Reuse already-vendored screenshots when available."""
    known = {
        "fire_lines": ROOT / "assets" / "img" / "fire-lines.png",
    }
    for objectid, src in known.items():
        dest = SHOT_DIR / f"{objectid}.jpg"
        if src.exists() and (not dest.exists() or dest.stat().st_size < 2000):
            subprocess.run(
                ["convert", str(src), "-quality", "85", str(dest)],
                check=False,
                capture_output=True,
            )
            print(f"Seeded screenshot for {objectid} from {src}", flush=True)


def main() -> None:
    seed_known_screenshots()
    rows = []
    for item in ITEMS:
        print(f"Processing {item['objectid']} ({item['kind']})...", flush=True)
        has_shot = False
        if item["kind"] == "project" and item.get("screenshot_url"):
            out = SHOT_DIR / f"{item['objectid']}.jpg"
            if out.exists() and out.stat().st_size > 2000:
                print("  using existing screenshot", flush=True)
                has_shot = True
            else:
                print(f"  capturing {item['screenshot_url']}", flush=True)
                has_shot = capture_screenshot(item["screenshot_url"], out)
                time.sleep(0.3)
            if has_shot:
                print(f"  screenshot ok ({out.stat().st_size} bytes)", flush=True)
            else:
                print("  falling back to record (no screenshot)", flush=True)
        rows.append(build_row(item, has_shot))

    with META_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {META_PATH}", flush=True)


if __name__ == "__main__":
    main()
