from flask import Flask, render_template, request, redirect, send_file
from extractors.web_scrapper_remoteok import extract_rmo_jobs
from extractors.web_scrapper_wework import extract_wwr_jobs
from extractors.download import download_file

app = Flask("JobScrapper")

@app.route("/")
def home():
  return render_template("home.html")

db = {}

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword in db:
    jobs = db[keyword]
    # print(len(db[keyword]))
  else:
    rmo = extract_rmo_jobs(keyword)
    wwr = extract_wwr_jobs(keyword)
    jobs = rmo + wwr
    db[keyword] = jobs
    # print(len(db[keyword]))
  return render_template("search.html", keyword = keyword, jobs = jobs)


@app.route("/export")
def download():
  keyword = request.args.get("keyword")
  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
  if keyword == None:
    return redirect("/")
  else:
    jobs = db[keyword]
    download_file(keyword, jobs)
  return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0")

