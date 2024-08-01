import json,re,io,gzip,sys
from urllib import request as rq,error

def main(module_string):
    match = re.match(r'^(?P<name>[a-zA-Z0-9_\-]+)(?P<version>\d[\d\.]*)?$', module_string)
    get_modules = match.group('name')
    modules_version = match.group('version') if match.group('version') else None

    if modules_version:
        request = rq.Request("https://pypi.org/pypi/{}/{}/json".format(get_modules, modules_version))
    else:
        request = rq.Request("https://pypi.org/pypi/{}/json".format(get_modules))
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    request.add_header('Accept-Encoding', 'gzip, deflate, br')
    try:
        res = rq.urlopen(request,timeout=5).read()
        buf = io.BytesIO(res)
        with gzip.GzipFile(fileobj=buf) as f:
            response_text = f.read().decode('utf-8')
            print(json.loads(response_text)['info']['requires_dist'])
    except error.HTTPError as e:
        print(f'HTTP error: {e.code} {e.reason}')
    except error.URLError as e:
        print(f'URL error: {e.reason}')
    except Exception as e:
        print(f'General error: {e}')

if __name__ == '__main__':
    main(sys.argv[1:][0])