from random import seed
from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

seed_url = "https://www.sec.gov/news/pressreleases"

urls = [seed_url]  # queue of urls to crawl
seen = [seed_url]  # stack of urls seen so far
opened = []  # we keep track of seen urls so that we don't revisit them
result = {}
url_names = []

maxNumUrl = 20  # set the maximum number of urls to visit
print("Starting with url="+str(urls))

while len(urls) > 0 and len(result) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url = urls.pop(0)
        if curr_url != seed_url:
            curr_url_name = url_names.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(
            curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()  # get the content
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue  # skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  # creates object soup
    text = soup.get_text().lower() # extracts all text found in a page
    if 'charges' in text and curr_url not in result and curr_url != seed_url:
        result[curr_url] = curr_url_name

    # Put child URLs into the stack
    for tag in soup.find_all('a', href=True):  # find tags with links
        childUrl = tag['href']  # extract just the link
        o_childurl = childUrl
        # join two urls use domain infomation from seed_url and use it to combine with childurl.
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        # if a childurl in a different domain, then unable to join
        # relative urls (not exactly the same as seedurl), can still join
        # make sure can stay within the business school domain
        print("seed_url=" + seed_url)
        print("original childurl=" + o_childurl)
        print("childurl=" + childUrl)
        print("seed_url in childUrl=" + str(seed_url in childUrl))
        print("Have we seen this childUrl=" + str(childUrl in seen))
        if 'https://www.sec.gov/news/press-release/' in childUrl and childUrl not in seen:
            # print("***urls.append and seen.append***")
            seen.append(childUrl)
            urls.append(childUrl)
            url_names.append(tag.text)
        else:
            print("######")

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
# print("List of seen URLs:")
# for seen_url in seen:
#     print(seen_url)
# print("List of opened URLs:")
# for opened_url in opened:
#     print(opened_url)
print("List of target URLs:")
for target_url, text in result.items():
    print(target_url, '\n', text, '\n******************************')