from flask import Flask, render_template, request, redirect, send_file
import requests
from bs4 import BeautifulSoup
from scrapers import Scrapers

app = Flask(__name__)
scraper = Scrapers()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword", "").strip()  # Get keyword from input
    if not keyword:
        return render_template("search.html", error="Please provide a keyword.")

    print("keyword:",keyword)

    berlin_jobs = scraper.berlin(keyword)
    wework_jobs = scraper.wework(keyword)
    # print(wework_jobs)
    web3_jobs = scraper.web3(keyword)

    return render_template("search.html", keyword=keyword, berlin_jobs=berlin_jobs, wework_jobs=wework_jobs, web3_jobs=web3_jobs)



if __name__ == "__main__":
    app.run(host="localhost", port=4000)