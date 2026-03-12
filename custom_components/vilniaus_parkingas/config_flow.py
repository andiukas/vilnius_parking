import aiohttp
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, API_URL

async def _fetch_lots():
    """Bendra funkcija aikštelėms gauti."""
    try:
        async with aiohttp.ClientSession() as session:
            params = {
                "where": "1=1", 
                "outFields": "pavadinimas", 
                "f": "json", 
                "returnDistinctValues": "true"
            }
            async with session.get(API_URL, params=params, timeout=10) as response:
                data = await response.json()
                return sorted([
                    f["attributes"]["pavadinimas"] 
                    for f in data.get("features", []) 
                    if f["attributes"].get("pavadinimas")
                ])
    except:
        return []

class VilniusParkingFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Vilniaus parkingas", data=user_input)

        lots = await _fetch_lots()
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("parking_lots", default=[]): cv.multi_select({lot: lot for lot in lots})
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        # KLAIDOS TAISYMAS: Nebesiunčiame config_entry kaip argumento
        return VilniusParkingOptionsFlowHandler()


class VilniusParkingOptionsFlowHandler(config_entries.OptionsFlow):
    """Tvarko 'Configure' mygtuką."""

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            # Atnaujiname pagrindinius duomenis per self.config_entry
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=user_input
            )
            return self.async_create_entry(title="", data={})

        lots = await _fetch_lots()
        # self.config_entry dabar pasiekiamas automatiškai per bazinę klasę
        current_lots = self.config_entry.data.get("parking_lots", [])

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("parking_lots", default=current_lots): cv.multi_select({lot: lot for lot in lots})
            })

        )
