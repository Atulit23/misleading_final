from turtle import goto
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright
from googlesearch import search

def extract_all_text(page):
    return page.evaluate(
        """() => {
        let result = '';
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        let node;
        while ((node = walker.nextNode())) {
            result += node.textContent + ' ';
        }
        return result.trim();
    }"""
    )


def google_search(query):
    encoded_query = urlencode({"q": query})
    for j in search(encoded_query, num_results=10):
        if not isinstance(j, str):
            if "amazon" not in j.url and "flipkart" not in j.url:
                return j.url
        else:
            if "amazon" not in j and "flipkart" not in j:
                return j

    return None


# Agar bande ko directly URL daalna ho
# https://www.amazon.com/HP-Students-Business-Quad-Core-Storage/dp/B0B2D77YB8/ref=sr_1_5
url = input("Please enter the URL : ")

with sync_playwright() as p:

    if "amazon" in url:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)
        product_title = page.locator('span[id="productTitle"]')
        product_title = product_title.text_content().strip().split("|")[0]
        print(product_title)

        product_description = page.locator(
            'div[id="feature-bullets"] ul[class="a-unordered-list a-vertical a-spacing-mini"]'
        ).text_content()

        print(product_description)

    if "flipkart" in url:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)
        product_title = page.locator('span[class="B_NuCI"]')
        product_title = product_title.text_content().strip().split("(")[0]
        print(product_title)
        product_description = page.locator('div[class="_2418kt"] ul').text_content()

        print(product_description)

    # Google search wala part
    url = google_search(product_title)
    if url is not None:
        page = browser.new_page()
        page.goto(url)
        p_elements = page.query_selector_all("p")

        everything = []
        for p_element in p_elements:
            everything.append(p_element.inner_text())

        span_elements = page.query_selector_all("span")
        for span_element in span_elements:
            everything.append(span_element.inner_text())

        descriptionToBeVerified = []

        for thing in everything:
            thing = thing.strip()
            if len(thing) > 20:
                descriptionToBeVerified.append(thing)

        if len(descriptionToBeVerified) < 1:
            final = extract_all_text(page)

        else:
            final = ""
            for things in descriptionToBeVerified:
                final += things

        print(final)

    browser.close()
