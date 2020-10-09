"""Config flow for Network Explorer integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT
)
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import DiscoveryInfoType, Optional
from homeassistant.helpers.network import get_url

from .const import (
    DEFAULT_PORT,
    DOMAIN
)
from homeassistant.components.media_player.const import (
    DOMAIN as MP_DOMAIN
)    

_LOGGER = logging.getLogger(__name__)

@config_entries.HANDLERS.register(DOMAIN)
class NetworkExplorerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self.data_schema = {
            vol.Required(CONF_NAME): str,
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): str,
       }

    '''
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        print("Does this get called?")
        return []
    '''

    async def async_step_user(self, user_input=None, errors=None):
        if user_input is not None:
            return self.async_create_entry(            
                title=user_input["name"],
                 data={
                CONF_NAME: user_input[CONF_NAME],
                CONF_HOST: user_input[CONF_HOST],
                CONF_PORT: user_input[CONF_PORT],
            },)


        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(self.data_schema)
        )  
        '''
        data_schema = vol.Schema(
            {
                vol.Required("setup_method", default="loo"): vol.In(
                    ["loo", "foo"]
                )
            }
        )
        '''
        '''
        return self.async_create_entry(
            title="Network Explorer Config",
            data={
                CONF_NAME: '',
                CONF_HOST: '',
                CONF_PORT: DEFAULT_PORT
            }
        )
        '''
