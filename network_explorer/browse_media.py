import requests
from homeassistant.components.media_player import BrowseMedia
from homeassistant.components.media_player.const import (
    MEDIA_CLASS_APP,
    MEDIA_CLASS_CHANNEL,
    MEDIA_CLASS_DIRECTORY,
    MEDIA_TYPE_APP,
    MEDIA_TYPE_APPS,
    MEDIA_TYPE_CHANNEL,
    MEDIA_TYPE_CHANNELS,
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

def item_payload(item):
        title = item['short']
        media_content_id = f'http://192.168.20.99:8002/api/directories/{title}'
        media_content_type = 'music'
        media_class =  MEDIA_CLASS_DIRECTORY
        return BrowseMedia(
        title=title,
        media_class=media_class,
        media_content_type=media_content_type,
        media_content_id=media_content_id,
        can_play=False,
        can_expand=True,
        thumbnail=None,
    )






async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def library_payload(media_content_type, media_content_id):
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
        d = [x['short'] for x in r]
        #print(d)
        for x in r:
            library_info.children.append(item_payload(x))

    return library_info    
