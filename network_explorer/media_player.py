import logging

import voluptuous as vol
from .const import DOMAIN as NETWORK_EXPLORER_DOMAIN
from homeassistant.components.media_player import PLATFORM_SCHEMA, MediaPlayerEntity, BrowseMedia
from homeassistant.components.media_player.const import (
    DOMAIN,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_BROWSE_MEDIA,
    SUPPORT_PLAY_MEDIA,
    MEDIA_TYPE_MUSIC,
    MEDIA_TYPE_TRACK,
    SERVICE_PLAY_MEDIA 
)

from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_SUPPORTED_FEATURES,
    CONF_NAME,
    CONF_STATE,
    STATE_OFF,
    STATE_ON,
    STATE_IDLE,
    EVENT_HOMEASSISTANT_START,
    SERVICE_TURN_ON,
    SERVICE_TURN_OFF
)

from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT
)

from homeassistant.core import EVENT_HOMEASSISTANT_START, callback

from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.event import async_track_state_change

from .browse_media import build_item_response, library_payload, menu_payload, players_payload

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string
    },
    extra=vol.REMOVE_EXTRA,
)

_LOGGER = logging.getLogger(__name__)

SUPPORT_NETWORK_EXPLORER = (SUPPORT_TURN_OFF | SUPPORT_TURN_ON | SUPPORT_BROWSE_MEDIA| SUPPORT_PLAY_MEDIA)

async def async_setup_entry(hass, entry, async_add_entities):
    name = entry.data[CONF_NAME]
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    player = NetworkExplorerMediaPlayer(hass, name, host , port)
    async_add_entities([player])

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    name = config.data[CONF_NAME]
    host = config.data[CONF_HOST]
    port = config.data[CONF_PORT]
    player = NetworkExplorerMediaPlayer(hass, name, host , port)
    async_add_entities([player])

class NetworkExplorerMediaPlayer(MediaPlayerEntity):
    def __init__(self, hass, name, host, port):
        self.hass = hass
        self._state = STATE_OFF
        self._name = name
        self.host = host
        self.port = port
        #self._unique_id = self._name.replace(" ", "_")
    

    async def async_added_to_hass(self):        
        """Subscribe to state changes."""
        _LOGGER.info("REGISTERING NETWORK_EXPLORER")

        @callback
        def async_on_dependency_update(*_):
            """Update ha state when dependencies update."""
            self.async_schedule_update_ha_state(True)

        @callback
        def async_on_network_explorer_update(event, updates):
            """Update ha state when dependencies update."""
            #result = updates.pop().result
            _LOGGER.info("UPDATE")

        @callback    
        def network_explorer_player_startup(event):
            _LOGGER.info("STARTUP NETWORK EXPLORER")
            async_track_state_change(self.hass, self._state, async_on_network_explorer_update)


        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, network_explorer_player_startup)

    @property
    def name(self):
        #print(self._name)
        #print(self.entity_id)
        return self._name

    '''
    @property
    def unique_id(self):
        """Return a unique ID."""
        print("UNIQUE ID")
        print(self._unique_id)
        print(self.entity_id)
        return self._unique_id
    '''

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        _LOGGER.info("SUPPORTED FEATURES:")
        return SUPPORT_NETWORK_EXPLORER

    async def async_update(self):
        _LOGGER.info("update network_explorer:")
    
    def turn_on(self):
        _LOGGER.info('ABout to turn on')
        #unique_id = self._unique_id
        self.hass.states.set(f'{self.entity_id}', STATE_IDLE)
        self._state = STATE_ON
        return True

    def turn_off(self):
        ('ABout to turn off')
        self._state = STATE_OFF
        #unique_id = self._unique_id
        self.hass.states.set(f'{self.entity_id}', STATE_OFF)
        return True


    async def async_browse_media(self, media_content_type=None, media_content_id=None):
        print(media_content_type, media_content_id)
        if media_content_id == None:
            return await menu_payload()
            #media_content_id = "http://192.168.20.99:8002/api/directories"
        elif media_content_type == 'library' and media_content_id.endswith('/api/home'):
            return await menu_payload()
        elif media_content_type == 'library' and media_content_id.endswith('/ha/playersfull'):
            mediaentities = self.hass.data[DOMAIN].entities
            #print(list(mediaentities))
            players = [x.name for x in mediaentities if x.name not in self.hass.data[NETWORK_EXPLORER_DOMAIN]]            
            entities = self.hass.data[NETWORK_EXPLORER_DOMAIN]
            data = entities[self.name]
            return await players_payload(media_content_id, players, data)
        elif '/api/speakers/' in media_content_id:
            return await menu_payload()
        return await library_payload(media_content_type, media_content_id)


    def play_media(self,  media_type, media_id, **kwargs):
        _LOGGER.info(media_type)
        _LOGGER.info(media_id)
        _LOGGER.info(kwargs)

    async def async_play_media(self, media_type, media_id, **kwargs):
        """Play a piece of media."""
        service_data = {
            "entity_id": "media_player.rumpus_room_speaker",
            "media_content_id": media_id,
            "media_content_type": media_type
        }
        await self.hass.services.async_call(DOMAIN, SERVICE_PLAY_MEDIA, service_data)
