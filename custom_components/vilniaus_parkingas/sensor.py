import logging
import async_timeout
import aiohttp
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from .const import API_URL

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=2)

async def async_setup_entry(hass, config_entry, async_add_entities):
    # Paimame sąrašą iš config_entry.data
    parking_lots = config_entry.data.get("parking_lots", [])
    entities = [VilniusParkingSensor(lot) for lot in parking_lots]
    async_add_entities(entities, True)

class VilniusParkingSensor(SensorEntity):
    def __init__(self, parking_lot):
        self._parking_lot = parking_lot
        self._attr_name = f"Parking {parking_lot}"
        # Unikalus ID užtikrina, kad sensorius nebus dubliuojamas
        self._attr_unique_id = f"vln_park_{parking_lot.lower().replace(' ', '_')}"
        self._state = None
        self._attrs = {}

    @property
    def state(self): return self._state

    @property
    def extra_state_attributes(self): return self._attrs

    @property
    def unit_of_measurement(self): return "vietos"

    @property
    def icon(self): return "mdi:car-parking-lot"

    async def async_update(self):
        params = {
            "f": "json",
            "where": f"pavadinimas = '{self._parking_lot}'",
            "outFields": "vacant,capacity",
            "returnGeometry": "true",
            "outSR": "4326"
        }

        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(API_URL, params=params) as response:
                        data = await response.json()
                        if data and "features" in data and len(data["features"]) > 0:
                            feat = data["features"][0]
                            self._state = feat["attributes"]["vacant"]
                            geo = feat.get("geometry", {})
                            if "rings" in geo:
                                rings = geo["rings"][0][0]
                                self._attrs = {
                                    "latitude": rings[1],
                                    "longitude": rings[0],
                                    "capacity": feat["attributes"]["capacity"]
                                }
        except Exception as e:
            _LOGGER.error("Klaida atnaujinant %s: %s", self._parking_lot, e)