from fastapi import FastAPI, HTTPException
import json, os
from datetime import datetime

app = FastAPI(title="MBA Colleges Details API")

DATA_FILE = "mba_college_details_41_80_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        raise HTTPException(
            status_code=503,
            detail="Data not generated yet. Please wait."
        )

    last_updated = datetime.fromtimestamp(
        os.path.getmtime(DATA_FILE)
    ).isoformat()

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "last_updated": last_updated,
        "data": data
    }


@app.get("/")
def root():
    return {
        "status": "API running 🚀",
        "source": "GitHub Actions Auto Scraper"
    }


@app.get("/mba_colleges_details_41_80")
def get_all_data():
    return load_data()

@app.get("/mba_colleges_details_41_80/{section}")
def get_section(section: str):
    payload = load_data()
    colleges = payload["data"]   # LIST

    SECTION_ALIASES = {
        "course": "courses",
        "courses": "courses",
        "fee": "fees",
        "fees": "fees",
        "review": "reviews",
        "reviews": "reviews",
        "admission": "admission",
        "placement": "placement",
        "ranking": "ranking",
        "gallery": "gallery",
        "faculty": "faculty",
        "scholarship": "scholarships",
        "scholarships": "scholarships"
    }

    section_key = SECTION_ALIASES.get(section.lower())
    if not section_key:
        raise HTTPException(status_code=404, detail="Invalid section")

    result = []

    for college in colleges:
        if section_key in college:
            result.append(college[section_key])

    if not result:
        raise HTTPException(status_code=404, detail="Section not found")

    return result