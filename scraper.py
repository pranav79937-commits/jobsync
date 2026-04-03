import requests
from bs4 import BeautifulSoup

def get_jobs():
    url = "https://remoteok.com/remote-dev-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    rows = soup.find_all("tr", class_="job")

    for row in rows[:15]:
        try:
            title = row.find("h2").text.strip()
            company = row.find("h3").text.strip()
            link = "https://remoteok.com" + row.get("data-href")

            jobs.append({
                "title": title,
                "company": company,
                "location": "Remote",
                "link": link
            })
        except:
            continue

    # fallback
    if not jobs:
        jobs = [
            {"title": "Python Intern", "company": "Demo", "location": "Remote", "link": "#"}
        ]

    return jobs
