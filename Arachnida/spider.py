# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rdel-olm <rdel-olm@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/23 18:11:28 by rdel-olm          #+#    #+#              #
#    Updated: 2026/03/23 18:11:37 by rdel-olm         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


# Spider extracts images from a target website.
#
# Workflow summary:
# 1) Parse CLI arguments: URL, recursive mode (-r), depth limit (-l), output path (-p).
# 2) Fetch and parse HTML pages with BeautifulSoup.
# 3) Collect links/images, resolve relative paths with urljoin, and avoid duplicates.
# 4) Download only the mandatory image extensions: jpg/jpeg, png, gif, bmp.
#
# Default behavior downloads images from the provided URL only.
# Recursive behavior enables page traversal up to the selected depth (default: 5).
# Output directory defaults to ./data when -p is not provided.

import argparse
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

seen_urls = set()
saved_imgs = set()

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-l", type=int, default=5)
    parser.add_argument("-p", default="./data")
    return parser.parse_args()


def fetch_page(url):
    try:
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")
    except:
        return None


def extract_links(soup, base_url):
    links = []
    for tag in soup.find_all("a"):
        href = tag.get("href")
        if href:
            links.append(urljoin(base_url, href))
    return links


def extract_images(soup, base_url):
    images = []
    for tag in soup.find_all("img"):
        src = tag.get("src")
        if src:
            images.append(urljoin(base_url, src))
    return images


def save_image(img_url, folder):
    try:
        filename = img_url.split("/")[-1].split("?")[0]
        if not filename.lower().endswith(VALID_EXTENSIONS):
            return
        response = requests.get(img_url)
        if response.status_code == 200:
            filepath = os.path.join(folder, filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            print("Downloaded:", filename)
    except:
        pass


def scrape(url, depth, max_depth, folder):
    if depth > max_depth or url in seen_urls:
        return
    print("Visiting:", url)
    seen_urls.add(url)
    soup = fetch_page(url)
    if soup is None:
        return
    for img in extract_images(soup, url):
        if img not in saved_imgs:
            saved_imgs.add(img)
            save_image(img, folder)
    for link in extract_links(soup, url):
        scrape(link, depth + 1, max_depth, folder)


def main():
    args = get_args()
    if not os.path.exists(args.p):
        os.makedirs(args.p)
    if args.r:
        scrape(args.url, 0, args.l, args.p)
    else:
        soup = fetch_page(args.url)
        if soup:
            for img in extract_images(soup, args.url):
                if img not in saved_imgs:
                    saved_imgs.add(img)
                    save_image(img, args.p)


if __name__ == "__main__":
    main()
