from compiler.project1.engine import build_url_fa, build_email_fa
from compiler.fa.multi_dfa_runner import MultiDFARunner
import time


print('strict mode will find fewer urls but most of urls will be a real url')
print('if you disable strict mode, the count of urls found will be more, but it is possible a few of them be incorrect')
url_strict_mode = input('do you want to enable strict mode? (y/n)') == 'y'
print('strict mode: ', url_strict_mode)
file = input('full file path:')
url_fa = build_url_fa(url_strict_mode)
email_fa = build_email_fa()
count = 0


def on_match(result, index):
    global count

    for i in result:
        count += 1
        print(count, end=') ')
        print('email' if i == 0 else 'url', end='')
        print(': ' + str(result[i]) + ' - index: ' + str(index))

    r = [len(value) for value in result.values()]

    return max(r)


try:
    file = open(file, encoding="utf-8")
    content = file.read()
    st = time.time()

    MultiDFARunner.run(
        [email_fa, url_fa],
        content,
        on_match
    )

    print('execution time: ' + str(time.time() - st))
except FileNotFoundError:
    print('invalid file path')