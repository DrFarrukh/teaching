"""Instructor demo: a browser robot that logs in, browses categories, opens every book page and builds a dataset.

Runs ONLY against practice sites built for automation:
  * quotes.toscrape.com/login  - accepts ANY username/password
  * books.toscrape.com         - a demo book shop (1,000 books, 50 categories)

What it produces in demo_output/ (the whole lecture in one run):
  raw_html/             every page exactly as received (the RAW layer: never edited)
  books_catalogue.csv   one row per book: title, category, prices, tax, rating, stock, UPC, reviews, description...
  provenance.json       source, settings, timestamps, checksums of the CSV and every raw page
  quality_report.txt    explicit checks: duplicates, missing values, price arithmetic, ranges

Usage:   python demo_browser.py                       (visible Chrome, red cursor dot, 3 categories x 8 books)
         python demo_browser.py --headless            (no window, for testing)
         python demo_browser.py --categories Travel,Mystery,Poetry --per-category 25
         python demo_browser.py --all --headless      (every category, every book: about 1,000 pages)
Password is read from an environment variable, never hard-coded:
         DEMO_PASSWORD=anything python demo_browser.py
"""

import argparse
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import urllib3.util.connection as urllib3_connection
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

urllib3_connection.HAS_IPV6 = False  # some networks advertise IPv6 but stall on it

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "demo_output"
RAW = OUT / "raw_html"
UA = "CS808-classroom-demo (dr.farrukh89@gmail.com)"
PAUSE = 10  # seconds between the big steps: slow enough for the class to watch
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def pause(slow: bool, seconds: float = PAUSE) -> None:
    time.sleep(seconds if slow else 0.2)


# A red dot that follows the pointer, so the class can SEE the robot's mouse.
# Selenium only dispatches pointer events inside the page (your real OS cursor does not move),
# and the dot is lost on every page load, so it is re-injected after each navigation.
CURSOR_JS = """
if (!document.getElementById('demo-cursor')) {
  const d = document.createElement('div');
  d.id = 'demo-cursor';
  d.style.cssText = 'position:fixed;left:0;top:0;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;' +
    'background:rgba(220,40,40,.85);border:3px solid #fff;box-shadow:0 0 8px rgba(0,0,0,.6);' +
    'z-index:2147483647;pointer-events:none;transition:transform .08s;';
  document.documentElement.appendChild(d);
  document.addEventListener('mousemove', e => { d.style.left = e.clientX + 'px'; d.style.top = e.clientY + 'px'; }, true);
  document.addEventListener('mousedown', () => { d.style.transform = 'scale(.6)'; }, true);
  document.addEventListener('mouseup', () => { d.style.transform = 'scale(1)'; }, true);
}
"""


def show_cursor(driver) -> None:
    driver.execute_script(CURSOR_JS)


def glide_to(driver, element, slow: bool, ms: int = 1200) -> None:
    """Move the visible pointer to the element in one smooth, watchable motion."""
    show_cursor(driver)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", element)
    ActionChains(driver, duration=ms if slow else 50).move_to_element(element).perform()


def glide_click(driver, element, slow: bool, ms: int = 1200) -> None:
    glide_to(driver, element, slow, ms)
    time.sleep(0.3 if slow else 0)
    ActionChains(driver).click(element).perform()


class Archive:
    """Saves every page exactly as received and remembers its checksum (the raw layer)."""

    def __init__(self) -> None:
        RAW.mkdir(parents=True, exist_ok=True)
        for old in RAW.glob("*.html"):  # start clean so pages from an earlier run never mix in
            old.unlink()
        self.pages = []

    def save(self, driver, kind: str) -> None:
        html = driver.page_source.encode("utf-8")
        name = f"{len(self.pages) + 1:04d}_{kind}.html"
        (RAW / name).write_bytes(html)
        self.pages.append(dict(file=f"raw_html/{name}", url=driver.current_url, kind=kind,
                               retrieved_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                               bytes=len(html), sha256=hashlib.sha256(html).hexdigest()))


def parse_money(text: str) -> float:
    return float(re.sub(r"[^0-9.]", "", text))


def read_book(driver, category: str, listing_url: str) -> dict:
    """Extract every field from an open book page."""
    info = {}
    for row in driver.find_elements(By.CSS_SELECTOR, "table.table-striped tr"):
        info[row.find_element(By.TAG_NAME, "th").text] = row.find_element(By.TAG_NAME, "td").text
    avail = driver.find_element(By.CSS_SELECTOR, "p.availability").text
    stock = re.search(r"\((\d+) available\)", avail)
    try:
        desc = driver.find_element(By.XPATH, "//div[@id='product_description']/following-sibling::p").text
    except NoSuchElementException:
        desc = ""  # some books genuinely have no description
    rating_cls = driver.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class")
    return dict(
        category=category,
        title=driver.find_element(By.CSS_SELECTOR, "div.product_main h1").text,
        price_gbp=parse_money(driver.find_element(By.CSS_SELECTOR, "p.price_color").text),
        price_excl_tax=parse_money(info["Price (excl. tax)"]),
        price_incl_tax=parse_money(info["Price (incl. tax)"]),
        tax=parse_money(info["Tax"]),
        rating=RATINGS.get(rating_cls.split()[-1]),
        in_stock="In stock" in avail,
        stock_count=int(stock.group(1)) if stock else None,
        upc=info["UPC"],
        product_type=info["Product Type"],
        num_reviews=int(info["Number of reviews"]),
        description=desc,
        product_url=driver.current_url,
        image_url=driver.find_element(By.CSS_SELECTOR, "div.item.active img").get_attribute("src"),
        listing_page=listing_url,
        scraped_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def quality_report(df: pd.DataFrame) -> str:
    """Explicit checks, one line each: the same six dimensions as the lecture."""
    lines = ["QUALITY REPORT: books_catalogue.csv", "=" * 60, f"rows: {len(df)}   columns: {df.shape[1]}", ""]
    lines.append(f"[uniqueness]   duplicate UPCs:                    {int(df['upc'].duplicated().sum())}")
    lines.append(f"[uniqueness]   duplicate titles:                  {int(df['title'].duplicated().sum())}")
    lines.append(f"[completeness] books with no description:         {int((df['description'] == '').sum())}")
    lines.append(f"[completeness] missing values (other columns):    {int(df.drop(columns='description').isna().sum().sum())}")
    gap = (df["price_excl_tax"] + df["tax"] - df["price_incl_tax"]).abs()
    lines.append(f"[consistency]  excl. tax + tax != incl. tax:      {int((gap > 0.005).sum())}")
    lines.append(f"[consistency]  price_gbp != price incl. tax:      {int(((df['price_gbp'] - df['price_incl_tax']).abs() > 0.005).sum())}")
    lines.append(f"[validity]     price <= 0 or > 100:               {int((~df['price_gbp'].between(0.01, 100)).sum())}")
    lines.append(f"[validity]     rating outside 1-5:                {int((~df['rating'].between(1, 5)).sum())}")
    lines.append(f"[validity]     in stock but stock_count == 0:     {int(((df['in_stock']) & (df['stock_count'] == 0)).sum())}")
    lines.append(f"[validity]     distinct product types:            {sorted(df['product_type'].unique())}")
    lines.append(f"[validity]     distinct tax values:               {[float(t) for t in sorted(df['tax'].unique())]}  <- every book taxed 0?")
    lines.append(f"[validity]     books with 0 reviews:              {int((df['num_reviews'] == 0).sum())} of {len(df)}  <- is the field used?")
    lines.append(f"[range]        price: min {df['price_gbp'].min():.2f}  median {df['price_gbp'].median():.2f}  max {df['price_gbp'].max():.2f}")
    lines.append("")
    lines.append("books per category:")
    lines += [f"   {k:<22}{v}" for k, v in df["category"].value_counts().items()]
    lines.append("")
    lines.append("LIMITS: a practice shop with invented data. Prices are in GBP; nothing here is real stock or sales.")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--categories", default="Travel,Mystery,Poetry", help="comma-separated category names")
    ap.add_argument("--per-category", type=int, default=8, help="max books to open per category")
    ap.add_argument("--all", action="store_true", help="every category, every book (use with --headless)")
    args = ap.parse_args()
    slow = not args.headless

    opts = webdriver.ChromeOptions()
    opts.add_argument(f"--user-agent={UA}")
    if args.headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1200,900")
    driver = webdriver.Chrome(options=opts)  # Selenium 4 fetches a matching driver itself
    wait = WebDriverWait(driver, 15)
    OUT.mkdir(exist_ok=True)
    archive = Archive()
    books, started = [], datetime.now(timezone.utc)

    try:
        # 1. Log in, typing credentials like a person would
        driver.get("https://quotes.toscrape.com/login")
        show_cursor(driver)
        pause(slow)
        user_box = driver.find_element(By.ID, "username")
        glide_click(driver, user_box, slow)
        user_box.send_keys("student_demo")
        pass_box = driver.find_element(By.ID, "password")
        glide_click(driver, pass_box, slow)
        pass_box.send_keys(os.environ.get("DEMO_PASSWORD", "not-a-real-password"))
        pause(slow, 2)
        glide_click(driver, driver.find_element(By.CSS_SELECTOR, "input[type=submit]"), slow)
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
        archive.save(driver, "login")
        print("Logged in:", driver.current_url)
        pause(slow)

        # 2. Open the book shop and read the category list from the sidebar
        driver.get("https://books.toscrape.com/")
        show_cursor(driver)
        archive.save(driver, "home")
        sidebar = [a.text.strip() for a in driver.find_elements(By.CSS_SELECTOR, "div.side_categories ul li ul li a")]
        wanted = sidebar if args.all else [c.strip() for c in args.categories.split(",")]
        unknown = [c for c in wanted if c not in sidebar]
        if unknown:
            raise SystemExit(f"Unknown categories {unknown}. Available: {sidebar}")
        limit = None if args.all else args.per_category
        print(f"{len(sidebar)} categories on the site; visiting {len(wanted)}.")
        pause(slow, 3)

        # 3. For each category: click it, page through the list, open every book, read its fields
        for cat in wanted:
            driver.get("https://books.toscrape.com/")
            show_cursor(driver)
            glide_click(driver, wait.until(EC.element_to_be_clickable((By.LINK_TEXT, cat))), slow)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.product_pod")))
            archive.save(driver, f"list_{cat.replace(' ', '_')}")
            n_in_cat = 0
            while True:
                hrefs = [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, "article.product_pod h3 a")]
                listing_url = driver.current_url
                for href in hrefs:
                    if limit is not None and n_in_cat >= limit:
                        break
                    link = driver.find_element(By.CSS_SELECTOR, f"article.product_pod h3 a[href$='{href.split('/')[-2]}/index.html']")
                    glide_click(driver, link, slow, ms=600)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-striped")))
                    archive.save(driver, "book")
                    books.append(read_book(driver, cat, listing_url))
                    n_in_cat += 1
                    print(f"  [{cat}] {n_in_cat:>3}  {books[-1]['title'][:48]:<48} £{books[-1]['price_gbp']:.2f}")
                    driver.back()
                    show_cursor(driver)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.product_pod")))
                if limit is not None and n_in_cat >= limit:
                    break
                nxt = driver.find_elements(By.CSS_SELECTOR, "li.next a")  # pagination: 20 books per page
                if not nxt:
                    break
                glide_click(driver, nxt[0], slow)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.product_pod")))
                archive.save(driver, f"list_{cat.replace(' ', '_')}_next")
            pause(slow, 2)
    finally:
        driver.quit()

    # 4. Build the dataset, the quality report and the provenance record
    df = pd.DataFrame(books)
    csv_path = OUT / "books_catalogue.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    report = quality_report(df)
    (OUT / "quality_report.txt").write_text(report, encoding="utf-8")
    csv_bytes = csv_path.read_bytes()
    provenance = dict(
        source="https://books.toscrape.com/ (practice site)", login_site="https://quotes.toscrape.com/login (accepts any password)",
        method="Selenium + Chrome, one page at a time, honest User-Agent", user_agent=UA,
        settings=dict(categories=wanted, per_category=limit, headless=args.headless),
        started_utc=started.isoformat(timespec="seconds"), finished_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        licence="practice site built for scraping; invented data", rows=len(df),
        output=dict(file="books_catalogue.csv", bytes=len(csv_bytes), sha256=hashlib.sha256(csv_bytes).hexdigest()),
        raw_pages=archive.pages,
        known_limits="Invented catalogue; prices in GBP; a snapshot of one moment; only the visited categories.")
    (OUT / "provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    print("\n" + report)
    print(f"\nDone: {len(df)} books, {len(archive.pages)} raw pages in {OUT}")


if __name__ == "__main__":
    main()
