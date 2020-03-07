from flask import Flask, request
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from pprint import pprint
app = Flask(__name__)

# Initialize sites
api = API()

@app.route('/')
def hello():
    return api.get_sites()

@app.route('/api/sites')
def api_sites():
    return api.get_sites()


class API:
    tceq_sites_url = "https://www17.tceq.texas.gov/tamis/index.cfm?fuseaction=report.site_list&sort=AQS_SITE_CD&order=asc&formSub=1&cams=checked&TCEQRegion=checked&siteName=checked&strAddr=checked&cityName=checked&zipCode=checked&cntyName=checked&lat=checked&long=checked&latLongType=dec&actDT=checked&urbanArea=checked&ownByName=checked&EPARegistered=checked&showActiveOnly=1&regFilter=&cntyFilter=&camsFilter="
    

    def get_sites(self):
        dfs = pd.read_html(self.tceq_sites_url)
        table = dfs[-1]
        pprint(table)
        return table.to_json(orient="records")

    
    def get_html(self, timestamp=None):

        # Give default timestamp
        if timestamp == None:
            timestamp = datetime.now().astimezone(tz=self.local_tz).timestamp()

        # Generate date
        date = datetime.fromtimestamp(timestamp).astimezone(tz=self.local_tz)

        # Prepare JSON
        params = {
            'select_date': "user",
            'user_month': date.month - 1,  # TCEQ has a weird offset.
            'user_day': date.day,
            'user_year': date.year,
            'select_site': "|||" + str(self.site),
            'time_format': "24hr"
        }

        return requests.get(self.url, params=params).text


if __name__ == '__main__':
    app.run()