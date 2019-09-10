from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view

from pengajuankredit.models import PengajuanKredit


@api_view(["GET"])
def cek_status_kredit(request, username):
    #1. cek dulu di database, informasi user ini.
    try:
        data = PengajuanKredit.objects.get(username=username)
        # 2. jika ada, kembalikan informasi tersebut
        if data.kepuasaan >= 90:
            data = "Lolos, approval karena kepuasaan Anda >= 90%"
        else:
            data = "Gagal, disapproval karena kepuasaan Anda dibawah 90%"
    except Exception:
        data = 'Username tidak dikenal, lakukan scraping'
        #3. jika tidak, scraping, => simpan ke db, dan kembalikan informasi tersebut
        import requests
        from bs4 import BeautifulSoup
        response = requests.get('https://www.bukalapak.com/u/{}'.format(username))
        if response.status_code == 404:
            data = 'Username tidak ada di bukalapak'
        elif response.status_code == 200:
            data = 'Username ada di bukalapak, scraping in progress!'
            soup = BeautifulSoup(response.text, "html.parser")

            # cari merchant id
            merchant_id = soup.find(id="merchant-page")["data-merchant-id"]

            # cari auth-access-token
            access_token = soup.find("meta", {"name": "oauth-access-token"})["content"]
            # get data
            url = "https://api.bukalapak.com/stores/{}?access_token={}".format(
                merchant_id, access_token
            )
            response = requests.get(url)
            json_response = response.json()["data"]

            data = {}
            data["pembeli_puas"] = json_response["rejection"]
            data["jumlah_feedback"] = json_response["reviews"]
            data["terakhir_online"] = json_response["inactivity"]["last_appear_at"]
            data["waktu_kirim_pesanan"] = json_response["delivery_time"]

    return Response({"status": "{}".format(data),
                     "deskripsi": "TODO"
                     })
