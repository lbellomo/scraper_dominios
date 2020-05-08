import os
import csv
import sys
from datetime import datetime
from pathlib import Path
from base64 import b64encode

import requests
from bs4 import BeautifulSoup


def download_domains(date: str):
    """Download all doamins for a date."""
    items = []
    
    pag = 1
    more_data = True

    while more_data:
        print(f"Downloading date {date}, pag {pag:<3}, len(items): {len(items):<4}")
        r = requests.get(url.format(pag=pag, date=date), headers=headers)
        data = r.json()
        more_data = data["hay_mas_datos"]
        pag = data["sig_pag"]

        soup = BeautifulSoup(r.json()["html"])
        links = (a.text for a in soup.find_all("a"))
        people = (p.text for p in soup.find_all("p"))
        type_operations = (i["title"] for i in soup.find_all("i"))

        for i, j, k in zip(links, people, type_operations):
            items.append([i, j, k])

    return items


def write_csv(date: str, items: list, header_csv: list = None):
    """Write items to a csv"""
    print("Writing data...")

    if not header_csv:
        header_csv = ["dominio", "titular", "tipo_operacion"]

    with (out_path / f"{date}.csv").open("w") as f:
        writer = csv.writer(f)
        writer.writerow(header_csv)
        for item in items:
            writer.writerow(item)


GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]

headers_api_github = {"Authorization": f"token {GITHUB_TOKEN}"}

if __name__ == "__main__":

    out_path = Path("data")
    out_path.mkdir(exist_ok=True)

    headers = requests.utils.default_headers()
    headers[
        "User-Agent"
    ] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

    base_url = "https://www.boletinoficial.gob.ar/"

    # from 2014 to present. Get posilbe dates.
    year = datetime.now().year
    url_dates = base_url + f"calendario/dias_publicacion/{year}/cuarta"

    url = (
        base_url
        + "seccion/actualizar/cuarta?pag={pag}&ult_rubro=DOMINIOS%20PUBLICADOS%20ar&fechaPublicacion={date}"
    )

    r = requests.get(url_dates.format(year=year), headers=headers)
    posible_dates = r.text.replace("\\u0022", "")[2:-2].split(",")

    date = posible_dates[-1]
    if (out_path / f"{date}.csv").exists():
        print("Last date alredy download. Nothing to do.")
        sys.exit()

    items = download_domains(date)
    write_csv(date, items)

    message = f"Add data for date {date}"
    content = b64encode((out_path / f"{date}.csv").read_bytes())
    json_data = {"message": message, "content": content.decode()}

    url_api_github = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/contents/{str(out_path)}/{date}.csv"

    print("Uploading data")

    r = requests.put(url_api_github, headers=headers_api_github, json=json_data)
    r.raise_for_status()

    print("All done!")
