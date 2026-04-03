def remove_duplicates(jobs):
    seen = set()
    unique = []
    for j in jobs:
        key = (j["title"], j["company"])
        if key not in seen:
            seen.add(key)
            unique.append(j)
    return unique

def filter_jobs(jobs, keyword, location, role):
    return [
        j for j in jobs
        if (not keyword or keyword.lower() in j["title"].lower())
        and (location == "All" or location.lower() in j["location"].lower())
        and (role == "All" or role.lower() in j["title"].lower())
    ]

def sort_jobs(jobs, keyword, sort_by):
    if sort_by == "Relevance":
        return sorted(jobs, key=lambda j: keyword.lower() in j["title"].lower(), reverse=True)
    return jobs

def calculate_match(user, job):
    u = set(user.lower().split())
    j = set(job.lower().split())
    return int(len(u & j) / len(u) * 100) if u else 0
