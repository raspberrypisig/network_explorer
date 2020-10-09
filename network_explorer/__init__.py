"""Network Explorer Custom component."""
import asyncio
import logging

from homeassistant.core import callback
from .const import DOMAIN, PLATFORMS

# The domain of your component. Should be equal to the name of your component.
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    '''
    async def my_service(call):
        
        """My first service."""
        _LOGGER.debug('Boo')
        await hass.services.async_call('media_player','play_media', {'entity_id': 'media_player.rumpus_room_speaker','media_content_id': 'http://192.168.20.99:8002/test/topsecret/orinoco.mp3', 'media_content_type': 'music'})
  
    # Register our service with Home Assistant.
    
    hass.services.async_register(DOMAIN, 'first', my_service)

    """Setup our skeleton component."""
    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.async_set('explorer_media.status', 'Works!')
    '''
    # Return boolean to indicate that initialization was successfully.
    return True

async def async_setup_entry(hass, entry):
    title = entry.title
    hass.data[DOMAIN] = [{title: dict(entry.data)}]

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
    )


    return True  