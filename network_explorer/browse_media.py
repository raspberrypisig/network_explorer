import pprint
import requests
from homeassistant.components.media_player import BrowseMedia
from homeassistant.components.media_player.const import (
    MEDIA_CLASS_APP,
    MEDIA_CLASS_CHANNEL,
    MEDIA_CLASS_DIRECTORY,
    MEDIA_TYPE_APP,
    MEDIA_TYPE_APPS,
    MEDIA_TYPE_CHANNEL,
    MEDIA_TYPE_CHANNELS
)
CONTENT_TYPE_MEDIA_CLASS = {
    MEDIA_TYPE_APP: MEDIA_CLASS_APP,
    MEDIA_TYPE_APPS: MEDIA_CLASS_DIRECTORY,
    MEDIA_TYPE_CHANNEL: MEDIA_CLASS_CHANNEL,
    MEDIA_TYPE_CHANNELS: MEDIA_CLASS_DIRECTORY,
}

import aiohttp

def build_item_response(coordinator, payload):
    pass

def item_payload(item, media_class=MEDIA_CLASS_DIRECTORY, media_content_type='library', can_play=False, can_expand=True):
        title = item['short']
        #media_content_id = f'http://192.168.20.99:8002/api/directories/{title}'
        media_content_id = item['media_content_id']
        media_content_type = media_content_type
        media_class =  media_class
        return BrowseMedia(
        title=title,
        media_class=media_class,
        media_content_type=media_content_type,
        media_content_id=media_content_id,
        can_play=can_play,
        can_expand=can_expand,
        thumbnail=None,
    )

def menu_item_payload(title, media_content_type, media_content_id, thumbnail=None ):
        return BrowseMedia(
        title=title,
        media_class=MEDIA_CLASS_DIRECTORY,
        media_content_type=media_content_type,
        media_content_id=media_content_id,
        can_play=False,
        can_expand=True,
        thumbnail=thumbnail,
    )    
#http://www.pngall.com/wp-content/uploads/5/Video-Player-PNG-Picture.png

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def library_payload(media_content_type, media_content_id, host, port):
    library_info = BrowseMedia(
        media_class=MEDIA_CLASS_DIRECTORY,
        media_content_id=media_content_id,
        media_content_type="library",
        title="Network Explorer Library",
        can_play=False,
        can_expand=True,
        children=[],
    )

    async with aiohttp.ClientSession() as session:
        r =  await fetch(session, media_content_id)
        #print(r)
        #d = [x['short'] for x in r]
        #print(d)
        for x in r:
            title = x['short']
            content_id = f'http://{host}:{port}/api/directories/{title}'
            x['media_content_id'] = content_id
            library_info.children.append(item_payload(x))

        media_content_id = media_content_id.replace('api/directories', 'api/files')

        r =  await fetch(session, media_content_id)
        #print(r)
        #d = [x['short'] for x in r]
        #print(d)
        for x in r:
            title = x["short"]
            x["media_content_id"] = f'{media_content_id}/{title}'
            x["media_content_id"] = x["media_content_id"].replace('api/files/','')
            x["media_content_type"] = 'music'
            library_info.children.append(item_payload(x, MEDIA_CLASS_APP, 'music', can_play=True, can_expand=False))        

    #print("library info:")
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(library_info.as_dict())
    return library_info    

async def menu_payload(host, port):
    menu_info = BrowseMedia(
        media_class=MEDIA_CLASS_DIRECTORY,
        media_content_id=f"http://{host}:{port}/api/home",
        media_content_type="library",
        title="Network Explorer Library",
        can_play=False,
        can_expand=True,
        children=[],
    )

    menu_options = [
        {"title": "Select media player(None)", "media_content_id": f"http://{host}:{port}/ha/playersfull", "media_content_type": "library", "thumbnail": "https://fonts.gstatic.com/s/i/materialicons/cast/v7/24px.svg"},
        {"title": "Play song", "media_content_id": f"http://{host}:{port}/api/directories", "media_content_type": "directory", "thumbnail": "https://fonts.gstatic.com/s/i/materialicons/play_circle_outline/v6/24px.svg"},
        {"title": "Playlist", "media_content_id": f"http://www.example.com?mediaplayer", "media_content_type": "directory", "thumbnail": "https://fonts.gstatic.com/s/i/materialicons/playlist_play/v5/24px.svg"}
    ]

    for x in menu_options:
        menu_info.children.append(menu_item_payload(title=x["title"], media_content_type=x["media_content_type"], media_content_id=x["media_content_id"], thumbnail=x["thumbnail"]))

    return menu_info

async def players_payload(media_content_id, players, host, port):
    media_content_id_url = f'http://{host}:{port}/api/home'
    print(media_content_id_url)
    players_info = BrowseMedia(
        media_class=MEDIA_CLASS_DIRECTORY,
        media_content_id=media_content_id_url,
        media_content_type="library",
        title="Available Media Players",
        can_play=False,
        can_expand=True,
        children=[],
    )

    #async with aiohttp.ClientSession() as session:
    #    r =  await fetch(session, media_content_id)
    #    for x in r:
    #        players_info.children.append(menu_item_payload(title=x["short"], media_content_type="library", media_content_id=x["full"]))

    for player in players:
        playerurl = f'http://{host}:{port}/api/defaultplayer/{player}'
        players_info.children.append(menu_item_payload(title=player, media_content_type="library", media_content_id=playerurl))
    
    return players_info
            
async def getDefaultPlayer(host, port):
    async with aiohttp.ClientSession() as session:
        r =  await fetch(session, f'http://{host}:{port}/api/defaultplayer')
        return r

async def setPlayer(media_content_id):
    async with aiohttp.ClientSession() as session:
        await fetch(session, media_content_id)

