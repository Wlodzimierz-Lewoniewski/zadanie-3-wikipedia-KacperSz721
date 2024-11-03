import requests
from bs4 import BeautifulSoup

def search():
    wiki_name = input("Enter Wikipedia category name: ")
    url = "https://pl.wikipedia.org/wiki/Kategoria:" + wiki_name.replace(' ', '_')
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pages = soup.find("div", id="mw-pages")

        if pages:
            articles = [
                {"url": link["href"], "name": link["title"]}
                for link in pages.find_all("a") if "title" in link.attrs
            ]

            for idx in range(2):
                if idx < len(articles):
                    article = articles[idx]
                    full_url = "https://pl.wikipedia.org" + article["url"]
                    article_response = requests.get(full_url)
                    article_soup = BeautifulSoup(article_response.text, "html.parser")

                    content = article_soup.find('div', {'id': 'mw-content-text', 'class': 'mw-body-content'})
                    titles = []
                    if content:
                        anchor_tags = content.select('a:not(.extiw)')
                        titles = [anchor.get('title') for anchor in anchor_tags if anchor.get('title') and anchor.get_text(strip=True)]
                        titles = titles[:5]

                    content_text_div = article_soup.find("div", {"class": "mw-content-ltr mw-parser-output"})
                    image_tags = content_text_div.find_all("img", src=True)
                    image_urls = [img["src"] for img in image_tags[:3]]

                    refer = article_soup.find('span', {"id": "Przypisy"})
                    if refer:
                        references_list = refer.find_next_sibling("ol", class_="references")
                        external_links = references_list.select('a.external.text')
                        reference_urls = [link['href'].replace("&", "&") for link in external_links[:3]]
                    else:
                        reference_urls = []

                    cat = article_soup.find("div", {"id": "mw-normal-catlinks"}).find_all("a")
                    cat_names = [cat.get_text() for cat in cat[1:4]]

                    output_titles = " | ".join(titles)
                    output_images = " | ".join(image_urls)
                    output_references = " | ".join(reference_urls)
                    output_categories = " | ".join(cat_names)

                    print(output_titles)
                    print(output_images)
                    print(output_references)
                    print(output_categories)
                else:
                    print(f"Article {idx + 1}: Information not found")
        else:
            print("No pages")
    else:
        print(f"Status code: {response.status_code}")

if __name__ == "__main__":
    search()
