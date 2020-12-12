from compiler.project1.engine import build_email_fa, build_url_fa
from compiler.fa.dfa_runner import DFARunner
from urllib.request import Request, urlopen
import time
import gzip

print('strict mode will find fewer urls but most of urls will be a real url')
print('if you disable strict mode, the count of urls found will be more, but it is possible a few of them be incorrect')
url_strict_mode = input('do you want to enable strict mode? (y/n)') == 'y'
print('strict mode: ', url_strict_mode)
url_fa = build_url_fa(url_strict_mode)
email_fa = build_email_fa()

# queue = [input('enter an entry website url: ')]
queue = ["https://www.digikala.com/"]
visited = dict()
i = 0


def on_email_match(string, index):
    global i
    i += 1
    print(str(i) + ') email: ' + str(string) + '    index: ' + str(index))


def on_url_match(string, index):
    global i
    i += 1
    queue.append(string)
    print(str(i) + ') url: ' + str(string) + '    index: ' + str(index))


while len(queue):
    target = queue.pop(0)

    if target in visited:
        continue

    print(f"========== crawling { target } ==========")

    try:
        req = Request(target)
        # req.add_header('User-Agent', 'Mozilla/5.0')
        req.add_header('User-Agent', "AKDEV'S WEB CRAWLER (http://akdev.ir)")
        # content = urlopen(req).read().decode('utf-8')
        content = gzip.decompress(urlopen(req).read()).decode('utf-8')

        st = time.time()
        emails = DFARunner.run(url_fa, content, None)
        urls = DFARunner.run(email_fa, content, None)
        print(time.time() - st)
        print(emails)
        print(urls)
    except e:
        print(e)
        print(f"========== failed to crawl { target } ==========")

    break
    visited[target] = True
