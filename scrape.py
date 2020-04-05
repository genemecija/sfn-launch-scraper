from bs4 import BeautifulSoup
import requests
import json

def getLaunchSched():
    # Get html from Space Flight Now's launch schedule site
    r = requests.get(
        'https://spaceflightnow.com/launch-schedule/')

    # If successful do this
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        
        # Get launch dates
        dates = []
        for date in soup.find_all("span", {"class": "launchdate"}):
            dates.append(date.text)

        # Get launch mission info
        missions = []
        for mission in soup.find_all("span", {"class": "mission"}):
            vehicle = mission.text.split(' • ')[0]
            payload = mission.text.split(' • ')[1]
            missions.append({
                "vehicle" : vehicle,
                "payload" : payload
            })

        # Get launch metadata
        missionData = []
        for data in soup.find_all("div", {"class": "missiondata"}):
            launchWindow = data.text.split('\n')[0].split(': ')[1]
            launchSite = data.text.split('\n')[1].split(': ')[1]
            missionData.append({
                "launchWindow": launchWindow,
                "launchSite": launchSite
            })
            
        # Get launch descriptions
        missionDesc = []
        for desc in soup.find_all("div", {"class": "missdescrip"}):
            missionDesc.append(desc.text)

        # Iterate through launches and append JSON formatted data to launchSched array
        launchSched = []
        for i in range(0,len(dates)-1):
            launchSched.append(
                {
                    dates[i] : {
                        "vehicle": missions[i]["vehicle"],
                        "payload": missions[i]["payload"],
                        "launchWindow": missionData[i]["launchWindow"],
                        "launchSite": missionData[i]["launchSite"],
                        "desc": missionDesc[i]
                    }
                }
            )

        # Convert to JSON and return
        return(json.dumps(launchSched))
    else:
        # If request is unsuccessful, return status code
        return(f"Unable to get HTML. Response status code: {r.status_code}")


if __name__ == "__main__":
    response = getLaunchSched()
    print(response)