"""Recheck final PDF navigation and, optionally, the availability of external references."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

from external_links import check_external
from navigation import audit_pdf_links


def inspect_pdf(pdf, manifest_path=None, browser=False):
    import pymupdf as fitz
    pdf = Path(pdf)
    manifest_path = Path(manifest_path) if manifest_path else pdf.with_name(pdf.stem + '-navigation.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if sha256(pdf.read_bytes()).hexdigest() != manifest['pdf_sha256']:
        raise ValueError(f'{pdf.name}: hash do PDF diverge da exportação auditada')
    html_name = manifest['html_file']
    if Path(html_name).name != html_name:
        raise ValueError('HTML do manifesto deve estar na mesma pasta')
    html = manifest_path.parent / html_name
    if sha256(html.read_bytes()).hexdigest() != manifest['html_sha256']:
        raise ValueError(f'{html.name}: hash do HTML diverge da exportação auditada')
    result = audit_pdf_links(pdf, manifest['plan'])
    with fitz.open(pdf) as document:
        external = [link['uri'] for page in document for link in page.get_links() if link['kind'] == fitz.LINK_URI]
    report = {'pdf': str(pdf), 'navigation': result, 'external_urls': external}
    if browser:
        from browser_links import check_html_clicks
        report['browser'] = check_html_clicks(html, manifest['plan'])
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', nargs='+', type=Path)
    parser.add_argument('--manifest', type=Path, help='Manifesto explícito, somente quando há um PDF')
    parser.add_argument('--external', action='store_true', help='Conferir referências HTTPS; resultado é datado')
    parser.add_argument('--browser', action='store_true', help='Clicar no HTML, incluindo número, título e página do sumário')
    parser.add_argument('--timeout', type=float, default=12)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args(argv)
    if args.manifest and len(args.pdf) != 1:
        parser.error('--manifest explícito aceita somente um PDF')
    if not 0 < args.timeout <= 60:
        parser.error('--timeout deve ser maior que zero e no máximo 60 segundos')
    try:
        files = [inspect_pdf(pdf, args.manifest, args.browser) for pdf in args.pdf]
        result = {'files': files, 'passed': all(f['navigation']['passed'] and f.get('browser', {}).get('passed', True) for f in files)}
        if args.external:
            result['external'] = check_external([url for f in files for url in f['external_urls']], args.timeout)
            result['passed'] = result['passed'] and result['external']['passed']
        else:
            result['external'] = {'status': 'not-checked'}
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(text + '\n', encoding='utf-8')
        else:
            print(text)
        return 0 if result['passed'] else 1
    except (ValueError, KeyError, OSError) as error:
        print(f'Falha na auditoria de links: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
