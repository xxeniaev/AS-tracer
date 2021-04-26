import re
import shlex
import subprocess
import sys
import IP2Location


def traceroute(address):
    """
    function that takes domain name or ip makes request to cymru.com data base to get AS info
    :param address:
    :return: list of strings with hops info
    """
    pattern = re.compile(".*\d  \* \* \*")

    arguments = ["traceroute"] + address
    process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out = []
    stdout_iterator = iter(process.stdout.readline, b"")
    for element in stdout_iterator:
        hop_info_line = element.decode("utf-8")
        if not re.match(pattern, hop_info_line):
            out.append(hop_info_line)
            print(hop_info_line)
        else:
            break

    return out


def whois(ip):
    """
    function that takes ip and makes request to cymru.com data base using whois to get AS info
    :param ip: string of one of the ips
    :return: string which contains needed AS NAME
    """
    arg_str = ['-v {}'.format(ip)]
    arguments = shlex.split("whois -h whois.cymru.com --") + arg_str
    process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out = []
    stdout_iterator = iter(process.stdout.readline, b"")
    for a in stdout_iterator:
        out.append(a.decode("utf-8"))

    return out[1]


def get_ips(lines):
    pattern = re.compile("\d+\.\d+\.\d+\.\d+")

    ips = []
    for v in lines:
        ips.append(pattern.search(v).group())

    return ips


def get_as(whois_line):
    pattern = re.compile(".+(?=\\n)")

    whois_elements = whois_line.split("|")
    out = pattern.search(whois_elements[len(whois_elements) - 1]).group()

    return out


def make_table(ip_as_dict):
    with open("out.txt", "w") as f:
        f.write("|  Number  |         IP         |         AS         |          Country          "
                "|               Provider               |\n")
        i = 0
        for item in ip_as_dict:
            i += 1
            f.write("| " + str(i) + " " * (9 - len(str(i))) + "| " + str(item[0]) + " " * (19 - len(item[0])) +
                    "| " + str(item[1]) + " " * (19 - len(item[1])) + "| " + str(item[2]) + " " * (26 - len(item[2])) +
                    "| " + str(item[3]) + " " * (37 - len(item[3])) + "|\n")


if __name__ == '__main__':
    IP2LocObj = IP2Location.IP2Location()
    IP2LocObj.open(
        "IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-ISP-DOMAIN-NETSPEED-AREACODE-WEATHER-SAMPLE.BIN")

    addr = sys.argv[1]
    ip_list = get_ips(traceroute([addr]))

    pattern = re.compile("\d+")

    final = []
    for current in ip_list:
        country = IP2LocObj.get_country_long(current)
        provider = '-'
        if int(pattern.search(current).group(0)) < 100:
            provider = IP2LocObj.get_isp(current)
        final.append((current, get_as(whois(current)), country, provider))

    make_table(final)
