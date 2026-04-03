import requests
from bs4 import BeautifulSoup

# -------- SOURCE 1: RemoteOK --------
def get_remoteok_jobs():
    url = "https://remoteok.com/remote-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    rows = soup.find_all("tr", class_="job")

    for row in rows[:10]:
        try:
            jobs.append({
                "title": row.find("h2").text.strip(),
                "company": row.find("h3").text.strip(),
                "location": "Remote",
                "link": "https://remoteok.com" + row.get("data-href"),
                "source": "RemoteOK"
            })
        except:
            continue

    return jobs


# -------- SOURCE 2: Indeed (LIMITED DEMO SAFE) --------
def get_indeed_jobs():
    jobs = [
        {
            "title": "Python Developer",
            "company": "Indeed Demo",
            "location": "India",
            "link": "#",
            "source": "Indeed (Demo)"
        }
    ]
    return jobs


# -------- SOURCE 3: Internshala (SIMULATED) --------
def get_internshala_jobs():
    jobs = [
        {
            "title": "Data Science Intern",
            "company": "Internshala Demo",
            "location": "Remote",
            "link": "#",
            "source": "Internshala (Demo)"
        }
    ]
    return jobs


# -------- MAIN FUNCTION --------
def get_jobs():
    jobs = []

    jobs.extend(get_remoteok_jobs())
    jobs.extend(get_indeed_jobs())
    jobs.extend(get_internshala_jobs())

    return jobs
