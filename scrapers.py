import requests
from bs4 import BeautifulSoup


class Scrapers:
    def __init__(self):
        self.jobs_db = []  # To store scraped job data

    def get_soup(self, url):
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def berlin(self, keyword):
        """Scrape berlinstartupjobs.com for the given keywords."""
        url = f"https://berlinstartupjobs.com/skill-areas/{keyword}"
        
        print("berlin url:", url)
        soup = self.get_soup(url)

        jobs_data = []

        jobs = soup.find("ul", class_="jobs-list-items").find_all("div", class_="bjs-jlid__wrapper")

        if not jobs:
            return []

        for job in jobs:
            title = job.find("h4", class_="bjs-jlid__h").text.strip()
            detail_link = job.find("a")["href"]
            company_name = job.find("a", class_="bjs-jlid__b").text.strip()
            company_link = job.find("a", class_="bjs-jlid__b")["href"]

            skills_ = job.find("div", class_="links-box").find_all("a")
            skills = [skill.text.strip().replace('\n', '').replace('\t', '') for skill in skills_]

            job_description = job.find("div", class_="bjs-jlid__description").text.strip().replace('\n', '').replace('\t', '').replace('\xa0', '')

            job_data = {
                "title": title,
                "company": company_name,
                "skills": skills,
                "job_description": job_description,
                "detail_link": detail_link,
                "company_link": company_link,
            }
            jobs_data.append(job_data)
        
        return jobs_data


    def wework(self, keyword):
        url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}"
        print("Wework url:", url)
        soup = self.get_soup(url)

        #when there is no matched job, "no_results" class div exists
        no_results = soup.find("div", class_="no_results")
        if no_results:
            return []

        jobs = soup.find("section", class_ = "jobs").find_all("li")[:-1]
        jobs = [job for job in jobs if 'feature--ad' not in job.get('class', [])] # Filter out list items with class name 'feature--ad'

        jobs_data=[]

        for job in jobs:
            title = job.find("span",class_="title").text

            company, contract_type, region = job.find_all("span", class_="company")

            job_url = job.find("div", class_="tooltip--flag-logo").next_sibling
            if job_url:
                job_url = job_url["href"] # to extract attribute "href"

            job_data = {
                "title": title,
                "company": company.text,
                "contract_type": contract_type.text,
                "region": region.text,
                "url":f"https://weworkremotely.com/{job_url}",
            }
            jobs_data.append(job_data)
        return jobs_data

    def web3(self, keyword):
        url= f"https://web3.career/{keyword}-jobs"
        print("Web3 url: ", url)
        soup = self.get_soup(url)

        jobs_table = soup.find("table", class_ = "table table-borderless")
        if not jobs_table:
            return []

        jobs_rows = jobs_table.find("tbody", class_="tbody").find_all("tr", class_="table_row")
        jobs_data = []

        for row in jobs_rows:
            # Skip ads with id="sponsor_2"
            if row.get("id") == "sponsor_2":
                continue

            # Extract job detail link and title (first td)
            first_td = row.find_all("td")[0]
            title_anchor = first_td.find("a")
            title = title_anchor.find("h2").text.strip() if title_anchor else "N/A"
            detail_link = f"https://web3.career{title_anchor['href']}" if title_anchor and title_anchor.get("href") else "N/A"

            # Extract company name (second td)
            second_td = row.find_all("td")[1]
            company = second_td.find("h3").text.strip() if second_td and second_td.find("h3") else "N/A"

            # Extract work type (fourth td)
            fourth_td = row.find_all("td")[3]
            work_type = fourth_td.find("span").text.strip() if fourth_td and fourth_td.find("span") else "N/A"

            # Store extracted data
            job_data = {
                "title": title,
                "company": company,
                "work_type": work_type,
                "detail_link": detail_link,
            }
            jobs_data.append(job_data)

        return jobs_data
#berlin  https://berlinstartupjobs.com/skill-areas//
#wework https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=
#web3 https://web3.career/-jobs 