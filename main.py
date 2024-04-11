import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def download_file(url):
    response = requests.get(url)
    print("Headers: {}".format(response.headers))

    filename = url.split("/")[-1]
    new_filename = "epub_books/" + filename.replace("%20", "_")
    print("Filename: {}".format(new_filename))

    with open(new_filename, mode="wb") as file:
        file.write(response.content)
        print(f"Downloaded file {filename}")


def scrape_page(page_url):
    try:
        page = requests.get(page_url)
        # Parse the HTML content
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find all anchor tags
        books_free_element = soup.find("div", class_="field-item even")
        tags_free_books_element = books_free_element.find_all('a')

        counter = 0
        # Extract the href attribute from each tag
        for tag in tags_free_books_element:
            # tag_text = tag.get_text()
            tag_url = tag.get('href')
            domain_element = urlparse(tag_url).netloc

            if domain_element:
                if domain_element == "www.amazon.com":
                    print("Is amazon domain URL")
                else:
                    book_page = requests.get(tag_url)
                    book_soup = BeautifulSoup(book_page.content, 'html.parser')
                    book_link_elements = book_soup.select('h3 > a')

                    for epub_link in book_link_elements:
                        link_book_url = str(epub_link.get('href'))
                        if link_book_url.endswith(".epub"):
                            print(f"Link for epub book format: {link_book_url}")
                            download_file(link_book_url)
                            counter = counter + 1

        print(f"\n{counter} of {len(tags_free_books_element)} links was downloaded")

    except Exception as e:
        print(f"Exception:  {e}")


if __name__ == "__main__":
    # Make a request to the website
    url = input("Enter the URL that you want to crawl: ")
    scrape_page(url)