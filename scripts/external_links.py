"""Bounded public-reference checks; HTTP availability is a dated observation."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlparse
from urllib.request import Request, urlopen


def check_url(url, timeout=12):
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username is not None:
        return {'url': url, 'status': 'invalid', 'reason': 'URL HTTPS sem credenciais é obrigatória'}
    request = Request(url, headers={'User-Agent': 'AtelieDeEstudos-link-check/0.3.1'})
    try:
        with urlopen(request, timeout=timeout) as response:
            final = response.geturl()
            if urlparse(final).scheme != 'https':
                return {'url': url, 'status': 'invalid', 'reason': 'Redirecionamento para protocolo não seguro'}
            prefix = response.read(1024)
            if parsed.path.lower().endswith('.pdf') and b'%PDF-' not in prefix:
                return {'url': url, 'status': 'unexpected-content', 'http_status': response.status,
                        'reason': 'A URL de PDF não respondeu com arquivo PDF'}
            return {'url': url, 'status': 'ok', 'http_status': response.status, 'final_url': final}
    except HTTPError as error:
        return {'url': url, 'status': 'blocked' if error.code in (401, 403, 429) else 'http-error',
                'http_status': error.code, 'reason': 'Acesso não confirmado; não tratar como referência aprovada'}
    except (URLError, TimeoutError, OSError) as error:
        return {'url': url, 'status': 'unavailable', 'reason': type(error).__name__}


def check_external(urls, timeout=12):
    unique = sorted({urldefrag(url)[0] for url in urls})
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda url: check_url(url, timeout), unique))
    return {'checked_at': datetime.now(timezone.utc).isoformat(), 'urls': results,
            'count': len(results), 'passed': all(r['status'] == 'ok' for r in results)}
