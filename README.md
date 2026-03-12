<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/5/5f/Parking_icon.svg" width="100" alt="Parking Icon">
</p>

# Vilniaus parkingo aikštelių integracija (MParking)

Ši integracija skirta „Home Assistant“ platformai, leidžianti realiu laiku stebėti Vilniaus stovėjimo aikštelių (**m.Parking**) užimtumą.

## 🚀 Įdiegimas

1. **HACS:** Pridėkite šią saugyklą kaip pasirinktinę (custom repository):  
   [https://github.com/andiukas/vilnius_parking/](https://github.com/andiukas/vilnius_parking/)
2. **Integracija:** Po įdiegimo eikite į `Settings` -> `Devices & Services` -> `Add Integration`.
3. **Paieška:** Suraskite ir pasirinkite **Vilniaus parkingas**.
4. **Konfigūracija:** Laukelyje `parking_lots` iš sąrašo pasirinkite dominančias aikšteles (galima pažymėti kelias).

## 📊 Sukuriami atributai

Kiekvienas jutiklis (sensor) pateikia šiuos papildomus duomenis, kuriuos galite naudoti žemėlapiuose ar automatizacijose:

| Atributas | Reikšmė (Pavyzdys) | Aprašymas |
| :--- | :--- | :--- |
| `latitude` | `54.688082...` | Aikštelės platuma |
| `longitude` | `25.294002...` | Aikštelės ilguma |
| `capacity` | `108` | Bendras vietų skaičius |
| `friendly_name` | `Parking T. Kosciuškos g. 1A` | Aikštelės pavadinimas |
---
*Sukurta stebėti Vilniaus miesto parkavimo infrastruktūrą.*

