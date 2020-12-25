import re
from requests import get

URL_REGEX = r"(([hH][tT][tT][pP][sS]?://|[wW]{3}\.)[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+(/[^\(\)><\s%#\'\"]*)*)"
EMAIL_REGEX = r"([a-zA-Z0-9-._]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+)"
email_re = re.compile(EMAIL_REGEX)
url_re = re.compile(URL_REGEX)
count = 0

def print_result(result):
    global count
    count += 1
    print(str(count) + ') ' + result)

print('do you wanna search in a file or in a website?')

if input('enter "f" for file or "w" for website: (w/f)') == 'f':
    file = input('enter file path :')

    try:

        file = open(file, encoding="utf-8")
        content = file.read()
    except FileNotFoundError:
        print('file path is incorrect')

    for url in url_re.findall(content):
        print_result(url[0])
    for email in email_re.findall(content):
        print_result(email[0])

else:
    queue = [input('enter an entry website url: ')]
    visited = dict()

    while len(queue):
        target = queue.pop(0)

        if target in visited:
            continue

        print(f"========== crawling {target} ==========")

        try:
            content = get(target).text
            for url in url_re.findall(content):
                queue.append(url[0])
                print_result(url[0])
            for email in email_re.findall(content):
                print_result(email[0])
        except KeyboardInterrupt:
            print('Good Bye =(')
            break
        except:
            print(f"========== failed to crawl {target} ==========")

        visited[target] = True