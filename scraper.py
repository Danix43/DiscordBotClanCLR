import aiohttp
from bs4 import BeautifulSoup
import re
from sty import fg

class Scraper:

    async def check_factions(self):
        def process_results(results):
            factions_name = {
                "paramedics" : "Paramedici",
                "nr" : "News Reporters - NR",
                "ttc" : "The Tow Truck Company - TTC",
                "lstaxi": "Los Santos Taxi - LSTaxi",
                "lvtaxi": "Las Venturas - LVTaxi",
                "sftaxi" : "San Fierro Taxi - SFTaxi",
                "lsinstructors": "Los Santos School Instructors - LSSI",
                "lvinstructors": "Las Venturas School Instructors - LVSI",
                "sfinstructors": "San Fierro School Instructors - SFSI",
                "greenstreet" : "Green Street Bloods - GSB",
                "tsarbratva" : "The Tsar Bratva - TTB", 
                "verdant" : "Verdant Family - VDT",
                "vietnamese": "Vietnamese Boys - VTB",
                "reddragon" : "Red Dragon Triad - RDT",
                "southernpimps": "Southern Pimps - SP",
                "avispa" : "Avispa Rifa - Avispa",
                "69pier" : "69 Pier Mobs - 69PM",
                "elloco" : "El Loco Cartel - ELC",
                "lspd" : "Los Santos Police Departament - LSPD",
                "lvpd" : "Las Venturas Police Departament - LVPD",
                "sfpd" : "San Fierro Police Departament - SFPD",
                "fbi" : "Federal Bureau of Investigations - FBI",
                "ng" : "National Guard - NG",
                "hitmen" : "Hitmen Agency - HA",
                "mayor" : "Primar"
            }
            statusuri = {"Closed" : "Aplicatii: ❌ Inchise ❌", "Open" : "Aplicatii: ✅ Deschis ✅"} 

            processed_factions = dict()
            for key, value in results.items():
                processed_factions[factions_name[key]] = statusuri[value]

            return processed_factions

        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.rpg2.b-zone.ro/factions/index") as response:
                html = await response.text()

                soap = BeautifulSoup(html, "lxml")
                tables = soap.find_all("table", attrs={"class": "fullTable"})

                factions = dict()

                for table in tables:
                    for row in table.find_all("tr"):
                        try:
                            regex = "(/factions/view/)|(/factions/mixtRules)|(/factions/departmentRules)|(/factions/gangRules)|(/factions/peacefulRules)"
                            factions[re.sub(regex, "", row.a["href"])] = row.i["title"]
                        except TypeError:
                            pass
                
                return process_results(factions)
    
    async def check_turfs(self):
        def process_result(turf_dict):
            mafi = {
                "GSB" : "Green Street Bloods - GSB",
                "TTB" : "The Tsar Bratva - TTB", 
                "VDT" : "Verdant Family - VDT",
                "VTB": "Vietnamese Boys - VTB",
                "RDT" : "Red Dragon Triad - RDT",
                "SP": "Southern Pimps - SP",
                "ARF" : "Avispa Rifa - Avispa",
                "69PM" : "69 Pier Mobs - 69",
                "ELC" : "El Loco Cartel - ELC",
            }

            mafi_turfs = dict()

            for mafie in mafi:
                locatii = set()
                for k, v in turf_dict.items():
                    if v == mafie:
                        locatii.add(k)
                        mafi_turfs[mafi[v]] = locatii
            return mafi_turfs

        def count_turfs(turf_dict):
            turfs = turf_dict
            for key, value in turf_dict.items():
                try:
                    value.remove("Alliance Turf")
                except KeyError:
                    pass
                try:
                    value.remove("DeathMatch Turf")
                except KeyError:
                    pass
                turfs[key] = " - ".join(value) + "\n 👉🏻 Total: " + str(len(value))
            return turfs

        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.rpg2.b-zone.ro/wars/turfs") as response:
                html = await response.text()

            soap = BeautifulSoup(html, "lxml")
            print("seaching for map")
            turfs_map = soap.find("div", attrs={"class": "map"})

            turfs = dict(turf["title"].split(" - Owner: ") for turf in turfs_map.find_all("div", attrs={"class": "showTooltip turf"}))

            return count_turfs(process_result(turfs))


if __name__ == "__main__":
    Scraper().check_turfs()