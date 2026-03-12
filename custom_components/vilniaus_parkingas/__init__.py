from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from .const import DOMAIN

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Nustatoma integracija."""
    
    # 1. Patikriname, ar nereikia ištrinti senų sensorių, kurių nebėra sąraše
    await cleanup_removed_entities(hass, entry)

    # 2. Užregistruojame platformas
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # 3. Registruojame klausytoją nustatymų pasikeitimui
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    return True

async def cleanup_removed_entities(hass: HomeAssistant, entry: ConfigEntry):
    """Ištrina sensorius iš Home Assistant registro, jei jie buvo atžymėti."""
    entity_reg = er.async_get(hass)
    
    # Gauname visas šios integracijos sukurtas esybes (entities)
    entries = er.async_entries_for_config_entry(entity_reg, entry.entry_id)
    
    # Dabartinis aikštelių sąrašas nustatymuose
    current_lots = entry.data.get("parking_lots", [])
    # Sukuriame unikalų ID formatą palyginimui (tokį patį kaip sensor.py)
    current_unique_ids = [
        f"vln_park_{lot.lower().replace(' ', '_')}" 
        for lot in current_lots
    ]

    for entity in entries:
        if entity.unique_id not in current_unique_ids:
            # Jei sensoriaus ID nėra naujame sąraše - triname jį iš HA registro
            entity_reg.async_remove(entity.entity_id)

async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Perkrauname integraciją, kai pasikeičia nustatymai."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Ištrinama integracija."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)