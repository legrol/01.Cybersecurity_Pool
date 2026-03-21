# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rdel-olm <rdel-olm@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/15 19:36:34 by rdel-olm          #+#    #+#              #
#    Updated: 2026/03/15 21:35:19 by rdel-olm         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

visited_pages = set()
found_images = set()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("url")
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-l", type=int, default=5)
    parser.add_argument("-p", default="./data")

    return parser.parse_args()


def get_links(url):
    try:
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        links = []

        for tag in soup.find_all("a"):
            href = tag.get("href")

            if href:
                links.append(urljoin(url, href))

        return links

    except:
        return []


def get_images(url):
    try:
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        images = []

        for tag in soup.find_all("img"):
            src = tag.get("src")

            if src:
                images.append(urljoin(url, src))

        return images

    except:
        return []


ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")


def download_image(url, path):

    try:
        filename = url.split("/")[-1].split("?")[0]

        if not filename.lower().endswith(ALLOWED_EXTENSIONS):
            return

        response = requests.get(url)

        if response.status_code == 200:

            filepath = os.path.join(path, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print("Downloaded:", filename)

    except:
        pass


def crawl(url, depth, max_depth, path):

    if depth > max_depth:
        return

    if url in visited_pages:
        return

    print("Visiting:", url)

    visited_pages.add(url)

    images = get_images(url)

    for img in images:
        if img not in found_images:
            found_images.add(img)
            download_image(img, path)

    links = get_links(url)

    for link in links:
        crawl(link, depth + 1, max_depth, path)


def main():

    args = parse_args()

    url = args.url
    recursive = args.r
    depth = args.l
    path = args.p

    if not os.path.exists(path):
        os.makedirs(path)

    if recursive:
        crawl(url, 0, depth, path)
    else:
        visited_pages.add(url)
        images = get_images(url)
        for img in images:
            if img not in found_images:
                found_images.add(img)
                download_image(img, path)


if __name__ == "__main__":
    main()