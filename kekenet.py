import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin

def get_page(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  # 指定编码为 UTF-8
    return response.text

def extract_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.select_one('#content > div > div.infoMain > div.playerMain.w.hauto > div.playerNav > div > ul')
    if ul:
        links = [urljoin(base_url, li.a['href']) for li in ul.find_all('li')]
        return links
    return []


def extract_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_elem = soup.select_one('#content > div > div.infoMain > div.f-title')
    if title_elem:
        title = title_elem.text.strip()
        title = re.sub(r'^经典英语美文背诵100篇\(MP3\+中英字幕\) ', '', title)
        return title
    return None

def extract_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    content_elem = soup.select_one('#content > div > div.infoMain > div.f-y.w.hauto')
    if content_elem:
        paragraphs = []
        for p_elem in content_elem.find_all('p', recursive=False):
            paragraph = []
            for elem in p_elem.children:
                if isinstance(elem, str):
                    paragraph.append(elem.strip())
                elif elem.name == 'br':
                    paragraph.append('\n\n')
            paragraphs.append(' '.join(paragraph))
        return '\n\n'.join(paragraphs)
    return None


def extract_audio_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    audio_elem = soup.select_one('#mp3_fileurl')
    if audio_elem:
        return audio_elem['src']
    return None

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

def main():
    base_url = 'https://m.kekenet.com/Article/201502/359486.shtml'
    html = get_page(base_url)
    links = extract_links(html, base_url)
    for link in links:
        print('crape', link)
        page_html = get_page(link)
        title = extract_title(page_html)
        if not title:
            continue
        content = extract_content(page_html)
        if not content:
            continue
        audio_url = extract_audio_url(page_html)
        if not audio_url:
            continue
        # Save content to markdown file
        markdown_filename = f'{title}.md'
        with open(markdown_filename, 'w', encoding='utf-8') as file:
            file.write(content)
        # Download audio file
        audio_filename = f'{title}.mp3'
        download_file(audio_url, audio_filename)
        print(f'Downloaded {title}')

if __name__ == '__main__':
    main()
