# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para guardaserie - Thank you robalo!
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "guardaserie"
__category__ = "S"
__type__ = "generic"
__title__ = "Guarda Serie"
__language__ = "IT"

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'],
    ['Accept-Encoding', 'gzip, deflate']
]

host = "http://www.guardaserie.club/"


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.channels.guardaserie mainlist")

    itemlist = [Item(channel=__channel__,
                     action="ultimi",
                     title="[COLOR azure]Ultimi Episodi Aggiunti[/COLOR]",
                     url=host + "/aggiornamenti-serie-tv/",
                     thumbnail="http://i58.tinypic.com/2zs64cz.jpg"),
                Item(channel=__channel__,
                     action="fichas",
                     title="[COLOR azure]Lista Serie TV[/COLOR]",
                     url=host + "/lista-serie-tv-guardaserie/",
                     thumbnail="http://i58.tinypic.com/2zs64cz.jpg"),
                Item(channel=__channel__,
                     action="anime",
                     title="[COLOR azure]Anime[/COLOR]",
                     url=host + "/lista-serie-tv-guardaserie/",
                     thumbnail="http://2.bp.blogspot.com/-4AeDx37c3uQ/VAxIHDhm-9I/AAAAAAAABRA/BUnctEGpVYM/s1600/528900971.gif"),
                Item(channel=__channel__,
                     action="cartoni",
                     title="[COLOR azure]Cartoni Animati[/COLOR]",
                     url=host + "/lista-serie-tv-guardaserie/",
                     thumbnail="http://i.imgur.com/d9GffYm.png"),
                Item(channel=__channel__,
                     action="progs",
                     title="[COLOR azure]Programmi TV[/COLOR]",
                     url=host + "/lista-serie-tv-guardaserie/",
                     thumbnail="http://mujakovic.weebly.com/uploads/1/4/7/9/14799472/3787546.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     extra="serie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


def search(item, texto):
    logger.info("streamondemand.channels.guardaserie search")

    item.url = host + "/?s=" + texto

    try:
        # Se tiene que incluir aquí el nuevo scraper o crear una nueva función para ello
        return cerca(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla.
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def fichas(item):
    logger.info("streamondemand.channels.guardaserie fichas")

    itemlist = []

    # data = scrapertools.cache_page(item.url)

    ## Descarga la página
    data = re.sub(
        r'\t|\n|\r',
        '',
        scrapertools.anti_cloudflare(item.url, headers)
    )

    data = scrapertools.find_single_match(data, '<a[^>]+>Serie Tv</a><ul>(.*?)</ul>')

    patron = '<li><a href="([^"]+)[^>]+>([^<]+)</a></li>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 url=scrapedurl), tipo='tv'))

    return itemlist


def ultimi(item):
    logger.info("streamondemand.channels.guardaserie fichas")

    itemlist = []

    ## Descarga la página
    data = re.sub(
        r'\t|\n|\r',
        '',
        scrapertools.anti_cloudflare(item.url, headers)
    )
 #   data = scrapertools.cache_page(item.url)
    patron = '<p>Nuove Puntate delle SERIE TV, Aggiunte OGGI:</p>(.*?)<div id="disclamer">'
    data = scrapertools.find_single_match(data, patron)

    patron = '<li><a href="([^"]+)[^>]+>([^<]+)</a></li>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        fulltitle = scrapedtitle[:scrapedtitle.find('-')]
        scrapedurl = urlparse.urljoin(host, scrapedurl)
        scrapedthumbnail = ""

        itemlist.append(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 fulltitle=fulltitle,
                 show=fulltitle,
                 url=scrapedurl))

    return itemlist

def anime(item):
    logger.info("streamondemand.channels.guardaserie anime")

    itemlist = []

    # data = scrapertools.cache_page(item.url)

    ## Descarga la página
    data = re.sub(
        r'\t|\n|\r',
        '',
        scrapertools.anti_cloudflare(item.url, headers)
    )

    data = scrapertools.find_single_match(data, '<a[^>]+>Anime</a><ul>(.*?)</ul>')

    patron = '<li><a href="([^"]+)[^>]+>([^<]+)</a></li>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 url=scrapedurl,
                 thumbnail="http://www.itrentenni.com/wp-content/uploads/2015/02/tv-series.jpg"), tipo='tv'))

    return itemlist


def cartoni(item):
    logger.info("streamondemand.channels.guardaserie fichas")

    itemlist = []

    ## Descarga la página
    data = re.sub(
        r'\t|\n|\r',
        '',
        scrapertools.anti_cloudflare(item.url, headers)
    )

    data = scrapertools.find_single_match(data, '<a[^>]+>Cartoni</a><ul>(.*?)</ul>')

    patron = '<li><a href="([^"]+)[^>]+>([^<]+)</a></li>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 show=scrapedtitle,
                 thumbnail="http://www.itrentenni.com/wp-content/uploads/2015/02/tv-series.jpg"), tipo='tv'))

    return itemlist


def progs(item):
    logger.info("streamondemand.channels.guardaserie fichas")

    itemlist = []

    ## Descarga la página
    data = re.sub(
        r'\t|\n|\r',
        '',
        scrapertools.anti_cloudflare(item.url, headers)
    )

    data = scrapertools.find_single_match(data, '<a[^>]+>Programmi TV</a><ul>(.*?)</ul>')

    patron = '<li><a href="([^"]+)[^>]+>([^<]+)</a></li>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        itemlist.append(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 show=scrapedtitle,
                 thumbnail="http://www.itrentenni.com/wp-content/uploads/2015/02/tv-series.jpg"))

    return itemlist


def cerca(item):
    logger.info("streamondemand.channels.guardaserie fichas")

    itemlist = []

    ## Descarga la página
    data = re.sub(
        r'\t|\n|\r',
        '',
        scrapertools.anti_cloudflare(item.url, headers)
    )

    patron = '<div class="search_thumbnail">.*?<a class="search_link" href="([^"]+)" rel="bookmark" title="([^"]+)">.*?<img src="([^"]+)" />.*?</a>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)

        if scrapedtitle.startswith("Guarda "):
            scrapedtitle = scrapedtitle[7:]

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 show=scrapedtitle,
                 thumbnail=scrapedthumbnail), tipo='tv'))

    return itemlist


def episodios(item):
    logger.info("streamondemand.channels.guardaserie episodios")

    item.title = item.fulltitle

    itemlist = []

    ## Descarga la página
    data = re.sub(
        r'\t|\n|\r',
        '',
        scrapertools.anti_cloudflare(item.url, headers)
    )

    serie_id = scrapertools.get_match(data, 'id=([^"]+)" rel="nofollow" target="_blank"')

    data = scrapertools.get_match(data, '<div id="episode">(.*?)</div>')

    seasons_episodes = re.compile('<select name="episode" id="(\d+)">(.*?)</select>', re.DOTALL).findall(data)

    for scrapedseason, scrapedepisodes in seasons_episodes:

        episodes = re.compile('<option value="(\d+)"', re.DOTALL).findall(scrapedepisodes)
        for scrapedepisode in episodes:

            season = str(int(scrapedseason) + 1)
            episode = str(int(scrapedepisode) + 1)
            if len(episode) == 1: episode = "0" + episode

            title = season + "x" + episode + " - " + item.show

            # Le pasamos a 'findvideos' la url con tres partes divididas por el caracter "?"
            # [host+path]?[argumentos]?[Referer]
            url = host + "/wp-admin/admin-ajax.php?action=get_episode&id=" + serie_id + "&season=" + scrapedseason + "&episode=" + scrapedepisode + "?" + item.url

            itemlist.append(
                Item(channel=__channel__,
                     action="findvideos",
                     title=title,
                     url=url,
                     fulltitle=title,
                     show=item.show,
                     thumbnail=item.thumbnail))

    if config.get_library_support():
        itemlist.append(
            Item(channel=__channel__,
                 title="[COLOR azure]Aggiungi [/COLOR]" + item.title + "[COLOR azure] alla libreria di Kodi[/COLOR]",
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios",
                 show=item.show))
        itemlist.append(
            Item(channel=__channel__,
                 title="[COLOR azure]Scarica tutti gli episodi della serie[/COLOR]",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodios",
                 show=item.show))

    return itemlist


def findvideos(item):
    logger.info("streamondemand.channels.guardaserie findvideos")

    itemlist = []

    url = item.url.split('?')[0]
    post = item.url.split('?')[1]
    referer = item.url.split('?')[2]

    headers.append(['Referer', referer])

    data = scrapertools.cache_page(url, post=post, headers=headers)

    url = scrapertools.get_match(data.lower(), 'src="([^"]+)"')
    url = re.sub(r'embed\-|\-607x360\.html', '', url)

    server = url.split('/')[2].split('.')
    server = server[1] if len(server) == 3 else server[0]

    title = "[" + server + "] " + item.title

    itemlist.append(
        Item(channel=__channel__,
             action="play",
             title=title,
             url=url,
             server=server,
             fulltitle=item.fulltitle,
             show=item.show,
             folder=False))

    return itemlist
