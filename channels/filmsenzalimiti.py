# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para filmsenzalimiti
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# ------------------------------------------------------------
import re

from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod

__channel__ = "filmsenzalimiti"
__category__ = "F"
__type__ = "generic"
__title__ = "Film Senza Limiti (IT)"
__language__ = "IT"
__creationdate__ = "20120605"

DEBUG = config.get_setting("debug")

host = "http://www.filmsenzalimiti.click"


def isGeneric():
    return True


def mainlist(item):
    logger.info("[filmsenzalimiti.py] mainlist")

    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film Del Cinema[/COLOR]",
                     action="novedades",
                     extra="movie",
                     url="%s/genere/film" % host,
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Dvdrip[/COLOR]",
                     action="novedades",
                     extra="movie",
                     url="%s/genere/dvd-rip" % host,
                     thumbnail="http://repository-butchabay.googlecode.com/svn/branches/eden/skin.cirrus.extended.v2/extras/moviegenres/Box%20Sets%20HD.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film Sub Ita[/COLOR]",
                     action="novedades",
                     extra="movie",
                     url="%s/genere/subita" % host,
                     thumbnail="http://i.imgur.com/qUENzxl.png"),
                Item(channel=__channel__,
                     action="search",
                     extra="movie",
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     extra="serie",
                     action="novedades_tv",
                     url="%s/genere/serie-tv" % host,
                     thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/New%20TV%20Shows.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca Serie TV...[/COLOR]",
                     action="search",
                     extra="serie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]
    return itemlist


def categorias(item):
    logger.info("[filmsenzalimiti.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data, '<li><a href\="\#">Dvdrip per Genere</a>(.*?)</ul>')
    patron = '<li><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="novedades",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True))

    return itemlist


def search(item, texto):
    logger.info("[filmsenzalimiti.py] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        if item.extra == "movie":
            return novedades(item)
        if item.extra == "serie":
            return novedades_tv(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def novedades(item):
    logger.info("[filmsenzalimiti.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)

    patronvideos = '<div class="post-item-side"[^<]+'
    patronvideos += '<a href="([^"]+)"[^<]+<img src="([^"]+)"'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl)
        start = html.find("</b></center></div>")
        end = html.find("</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.get_filename_from_url(scrapedurl).replace("-", " ").replace("/", "").replace(
            ".html", "").capitalize().strip()
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='movie'))

    try:
        next_page = scrapertools.get_match(data, 'class="nextpostslink" rel="next" href="([^"]+)"')
        itemlist.append(
            Item(channel=__channel__,
                 action="novedades",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 extra=item.extra,
                 folder=True))
    except:
        pass

    return itemlist


def novedades_tv(item):
    logger.info("[filmsenzalimiti.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)

    patronvideos = '<div class="post-item-side"[^<]+'
    patronvideos += '<a href="([^"]+)"[^<]+<img src="([^"]+)"'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl)
        start = html.find("</b></center></div>")
        end = html.find("</p>", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        scrapedtitle = scrapertools.get_filename_from_url(scrapedurl).replace("-", " ").replace("/", "").replace(
            ".html", "").capitalize().strip()
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 folder=True), tipo='tv'))

    try:
        next_page = scrapertools.get_match(data, 'class="nextpostslink" rel="next" href="([^"]+)"')
        itemlist.append(
            Item(channel=__channel__,
                 action="novedades_tv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png",
                 extra=item.extra,
                 folder=True))
    except:
        pass

    return itemlist


def episodios(item):
    def load_episodios(html, item, itemlist, lang_title):
        patron = '((?:.*?<a href="[^"]+" class="external" rel="nofollow" target="_blank">[^<]+</a>)+)'
        matches = re.compile(patron).findall(html)
        for data in matches:
            # Extrae las entradas
            scrapedtitle = data.split('<a ')[0]
            scrapedtitle = re.sub(r'<[^>]*>', '', scrapedtitle).strip()
            if scrapedtitle != 'Categorie':
                scrapedtitle = scrapedtitle.replace('×', 'x')
                itemlist.append(
                    Item(channel=__channel__,
                         action="findvideos",
                         title="[COLOR azure]%s[/COLOR]" % (scrapedtitle + " (" + lang_title + ")"),
                         url=data,
                         thumbnail=item.thumbnail,
                         extra=item.extra,
                         fulltitle=scrapedtitle + " (" + lang_title + ")" + ' - ' + item.show,
                         show=item.show))

    logger.info("[filmsenzalimiti.py] episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = scrapertools.decodeHtmlentities(data)

    lang_titles = []
    starts = []
    patron = r"STAGIONE.*?ITA"
    matches = re.compile(patron, re.IGNORECASE).finditer(data)
    for match in matches:
        season_title = match.group()
        if season_title != '':
            lang_titles.append('SUB ITA' if 'SUB' in season_title.upper() else 'ITA')
            starts.append(match.end())

    i = 1
    len_lang_titles = len(lang_titles)

    while i <= len_lang_titles:
        inizio = starts[i - 1]
        fine = starts[i] if i < len_lang_titles else -1

        html = data[inizio:fine]
        lang_title = lang_titles[i - 1]

        load_episodios(html, item, itemlist, lang_title)

        i += 1

    if config.get_library_support() and len(itemlist) != 0:
        itemlist.append(
            Item(channel=__channel__,
                 title=item.title,
                 url=item.url,
                 action="add_serie_to_library",
                 extra="episodios" + "###" + item.extra,
                 show=item.show))
        itemlist.append(
            Item(channel=__channel__,
                 title="Scarica tutti gli episodi della serie",
                 url=item.url,
                 action="download_all_episodes",
                 extra="episodios" + "###" + item.extra,
                 show=item.show))

    return itemlist


def findvideos(item):
    logger.info("[filmsenzalimiti.py] findvideos")

    # Descarga la página
    data = item.url if item.extra == 'serie' else scrapertools.cache_page(item.url)

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist
