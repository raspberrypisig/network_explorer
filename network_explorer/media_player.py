import logging

import voluptuous as vol

from homeassistant.components.media_player import PLATFORM_SCHEMA, MediaPlayerEntity, BrowseMedia
from homeassistant.components.media_player.const import (
    DOMAIN,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_BROWSE_MEDIA,
    SUPPORT_PLAY_MEDIA,
    MEDIA_TYPE_MUSIC
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

from homeassistant.core import EVENT_HOMEASSISTANT_START, callback

from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.event import async_track_state_change

from .browse_media import build_item_response, library_payload

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string
    },
    extra=vol.REMOVE_EXTRA,
)

_LOGGER = logging.getLogger(__name__)

SUPPORT_NETWORK_EXPLORER = (SUPPORT_TURN_OFF | SUPPORT_TURN_ON | SUPPORT_BROWSE_MEDIA| SUPPORT_PLAY_MEDIA)

async def async_setup_entry(hass, entry, async_add_entities):
    name = entry.data["name"]
    player = NetworkExplorerMediaPlayer(hass, name)
    async_add_entities([player])

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    player = NetworkExplorerMediaPlayer(hass, name)
    async_add_entities([player])



class NetworkExplorerMediaPlayer(MediaPlayerEntity):
    def __init__(self, hass, name):
        self.hass = hass
        self._state = STATE_OFF
        self._name = name
    

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
            async_track_state_change(self.hass, self._state, async_on_network_explorer_update)


        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, network_explorer_player_startup)

    @property
    def name(self):
        return self._name

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
        name = self._name
        self.hass.states.set(f'{DOMAIN}.{name}', STATE_IDLE)
        self._state = STATE_ON
        return True

    def turn_off(self):
        _LOGGER.info('ABout to turn off')
        self._state = STATE_OFF
        name = self._name
        self.hass.states.set(f'{DOMAIN}.{name}', STATE_OFF)
        return True


    async def async_browse_media(self, media_content_type=None, media_content_id=None):
        if media_content_id == None:
            media_content_id = "http://192.168.20.99:8002/api/directories"
        print(media_content_type, media_content_id)
        return await library_payload(media_content_type, media_content_id)


