#!/usr/bin/env python

""" Transform Wordpress files to rst files. """
import argparse
import os
import sys
import time
import subprocess

from codecs import open


def build_markdown_header(title, date, author, categories, slug, lang, tags):
    """Build a header from a list of fields"""
    header = 'Title: %s\n' % title
    if date:
        header += 'Date: %s\n' % date
    if author:
        header += 'Author: %s\n' % author
    if categories:
        header += 'Category: %s\n' % ', '.join(categories)
    if tags:
        header += 'Tags: %s\n' % ', '.join(tags)
    if slug:
        header += 'Slug: %s\n' % slug
    if lang:
        header += 'Lang: %s\n' % lang
    header += '\n'
    return header


def build_dirname(filename, date):
    return os.path.join(str(date.tm_year), str(date.tm_mon), filename)


def wp2fields(xml):
    """Opens a wordpress XML file, and yield pelican fields"""
    try:
        from BeautifulSoup import BeautifulStoneSoup
    except ImportError:
        error = ('Missing dependency '
                 '"BeautifulSoup" required to import Wordpress XML files.')
        sys.exit(error)

    xmlfile = open(xml, encoding='utf-8').read()
    soup = BeautifulStoneSoup(xmlfile)
    items = soup.rss.channel.findAll('item')

    for item in items:

        if item.fetch('wp:status')[0].contents[0] == "publish":

            try:
                title = item.title.contents[0]
            except IndexError:
                continue

            content = item.fetch('content:encoded')[0].contents[0]
            filename = item.fetch('wp:post_name')[0].contents[0]
            link = item.fetch('link')[0].contents[0]
            name = link.strip("/").split("/")[-1]
            raw_date = item.fetch('wp:post_date')[0].contents[0]
            date_object = time.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
            date = time.strftime("%Y-%m-%d %H:%M", date_object)

            author = item.fetch('dc:creator')[0].contents[0]

            categories = [cat.contents[0] for cat in item.fetch(domain='category')]

            tags = [tag.contents[0] for tag in item.fetch(domain='post_tag')]

            yield (title, content, filename, date, date_object, author, categories, tags, "html")


def fields2pelican(fields, out_markup, output_path, dircat=False, strip_raw=False):
    lang = ['en', 'fr']
    for title, content, filename, date, date_object, author, categories, tags, in_markup in fields:
        for i, post in enumerate(content.split("<!--:fr-->")):
            ext = '.md'
            current_lang = lang[i]
            header = build_markdown_header(title, date, author, categories, filename, current_lang, tags)
            fullname = build_dirname(filename, date_object)

            try:
                os.makedirs(os.path.join(output_path, os.path.dirname(fullname)))
            except OSError:
                pass

            if current_lang != 'en':
                out_filename = os.path.join(output_path, fullname+"-"+current_lang+ext)
            else:
                out_filename = os.path.join(output_path, fullname+ext)

            print(out_filename)

            if in_markup == "html":
                html_filename = os.path.join(output_path, fullname+'.html')

                with open(html_filename, 'w', encoding='utf-8') as fp:
                    # Replace newlines with paragraphs wrapped with <p> so
                    # HTML is valid before conversion

                    # paragraphs = post.split('\n\n')
                    # paragraphs = [u'<p>{0}</p>'.format(p) for p in paragraphs]
                    # new_content = ''.join(paragraphs)

                    # TWEAK: Remove lang separator : <!--:-->
                    post = post.replace("<!--:-->", "")
                    post = post.replace("<!--:en-->", "")

                    fp.write(post)


                parse_raw = '--parse-raw' if not strip_raw else ''

                # Try to support the latest version of markdown
                strict = '--strict' if not out_markup == 'markdown_strict' else ''

                cmd = (
                    'pandoc --normalize --reference-links {parse_raw} {strict} --from=html'
                       ' --to={markup} -o "{out_filename}" "{html_filename}"').format(
                       parse_raw=parse_raw,
                       strict=strict,
                       markup=out_markup,
                       out_filename=out_filename,
                       html_filename=html_filename
                    )

                try:
                    rc = subprocess.call(cmd, shell=True)
                    if rc < 0:
                        error = "Child was terminated by signal %d" % -rc
                        exit(error)

                    elif rc > 0:
                        error = "Please, check your Pandoc installation."
                        exit(error)
                except OSError, e:
                    error = "Pandoc execution failed: %s" % e
                    exit(error)

                os.remove(html_filename)

                with open(out_filename, 'r', encoding='utf-8') as fs:
                    content = fs.read()

                    if out_markup == "markdown":
                        # In markdown, to insert a <br />, end a line with two or more spaces & then a end-of-line
                        content = content.replace("\\\n ", "  \n")
                        content = content.replace("\\\n", "  \n")

                        # TWEAK: replace \$ to $ because pelican doesn't support this syntax
                        content = content.replace("\$", "$")


            with open(out_filename, 'w', encoding='utf-8') as fs:
                fs.write(header + content)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(dest='input', help='The input file to read')
    parser.add_argument('-o', '--output', dest='output', default='output',
        help='Output path')
    parser.add_argument('-m', '--markup', dest='markup', default='markdown',
        choices=['rst', 'markdown', 'markdown_strict'],
        help='Output markup format (supports rst & markdown)')
    parser.add_argument('--dir-cat', action='store_true', dest='dircat',
        help='Put files in directories with categories name')
    parser.add_argument('--strip-raw', action='store_true', dest='strip_raw',
        help="Strip raw HTML code that can't be converted to "
             "markup such as flash embeds or iframes (wordpress import only)")
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.exists(args.output):
        try:
            os.mkdir(args.output)
        except OSError:
            error = "Unable to create the output folder: " + args.output
            exit(error)

    fields = wp2fields(args.input)

    fields2pelican(fields, args.markup, args.output,
                   dircat=args.dircat or False,
                   strip_raw=args.strip_raw or False)

if __name__ == "__main__":
    main()
