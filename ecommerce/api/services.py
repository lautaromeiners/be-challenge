import requests
from django.http import HttpResponse

def get_usd_price():
    response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')

    if response.status_code == 200:
        response = response.json()
        usd = response[1]['casa']['venta'].replace(',', '.')
        return float(usd)
    else:
        return HttpResponse("{'status': 'fail', 'msg': 'Fail to query Dolarsi service'}", content_type='aplication/json')
