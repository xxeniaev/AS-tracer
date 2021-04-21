import re
import shlex
import subprocess


def traceroute(arguments):
    pattern = re.compile(" \d  \* \* \*")

    with open("out.txt", "w") as f:
        process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_iterator = iter(process.stdout.readline, b"")
        for el in stdout_iterator:
            line = el.decode("utf-8")
            if not re.match(pattern, line):
                f.write(line)
                print(line)
            else:
                print('всё' + line)
                exit(0)


if __name__ == '__main__':
    traceroute(shlex.split("traceroute yandex.ru"))
