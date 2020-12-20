from compiler.project1.engine import build_email_fa, build_url_fa
from compiler.fa.multi_dfa_runner import MultiDFARunner
import requests
import time

print('strict mode will find fewer urls but most of urls will be a real url')
print('if you disable strict mode, the count of urls found will be more, but it is possible a few of them be incorrect')
url_strict_mode = input('do you want to enable strict mode? (y/n)') == 'y'
print('strict mode: ', url_strict_mode)
url_fa = build_url_fa(url_strict_mode)
email_fa = build_email_fa()

queue = [input('enter an entry website url: ')]
visited = dict()
count = 0


def on_match(result, index):
    global count

    for i in result:
        if i == 1:
            queue.append(result[i])

        count += 1
        print(count, end=') ')
        print('email' if i == 0 else 'url', end='')
        print(': ' + str(result[i]) + ' - index: ' + str(index))

    r = [len(value) for value in result.values()]

    return max(r)


while len(queue):
    target = queue.pop(0)

    if target in visited:
        continue

    print(f"========== crawling { target } ==========")

    try:
        content = requests.get(target).text
        st = time.time()

        MultiDFARunner.run(
            [email_fa, url_fa],
            content,
            on_match
        )

        print("execution time: " + str(time.time() - st))
    except:
        print(f"========== failed to crawl { target } ==========")

    visited[target] = True
