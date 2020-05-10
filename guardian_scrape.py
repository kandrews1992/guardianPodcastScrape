import requests
import wget 
from bs4 import BeautifulSoup
from pathlib import Path 

def makeOutputDir(dir=""):
    Path(dir).mkdir(parents=True, exist_ok=True)

def getPageLinks(url, tag="a", match_string="-podcast"):
    """ return a list of sub-pages to subsequently search for file file_exts 
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [] 
    # traverse anchors to find all tags with match_string
    for anchor in soup.find_all(tag, href=True):
        if anchor.text:
            if match_string in anchor['href']:
                links.append(anchor['href'])
    # remove any double entries
    links = list(dict.fromkeys(links))
    return links 

def getDownloads(url, outpath, tag="a", ext=".mp3"):
    links = getPageLinks(url)
    makeOutputDir(outpath)
    downloads = []  # store the links to each individual download link
    # loop over all sub-page urls 
    for url in links:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # loop over all tags and search for exts
        for anchor in soup.find_all(tag, href=True):
            if anchor.text:
                if ext in anchor['href']:
                    wget.download(anchor['href'], out=outpath)

if __name__=="__main__":
    url = "https://www.theguardian.com/news/series/the-audio-long-read"
    outpath = "output"
    getDownloads(url, outpath)
    
