import re
import datetime
from django.shortcuts import render
from django.utils import dateparse

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

            # kepuasan = positive / (positive + negative) * 100
            reviews = json_response["reviews"]
            positive = reviews["positive"]
            negative = reviews["negative"]
            kepuasan = (positive / (positive + negative)) * 100 

            jumlah_feedback = positive + negative

            terakhir_online = dateparse.parse_datetime(json_response["inactivity"]["last_appear_at"])

            bergabung = dateparse.parse_datetime(json_response["owner"]["joined_at"])

            # string, ambil integernya
            waktu_kirim_pesan = json_response["delivery_time"]
            waktu_kirim_pesan = int(re.match(r"\d+", waktu_kirim_pesan).group())
            jumlah_pengikut = json_response["subscriber_amount"]

            data = PengajuanKredit.objects.create(
                username=username,
                kepuasaan=kepuasan,
                jumlah_feedback=jumlah_feedback,
                jumlah_pengikut=jumlah_pengikut,
                terakhir_online=terakhir_online,
                bergabung=bergabung,
                waktu_kirim_pesan=waktu_kirim_pesan
            )

            if data.kepuasaan >= 90:
                data.approve = True
                data.save()
                data = "Lolos, approval karena kepuasaan Anda >= 90%"
            else:
                data.approve = False
                data.save()
                data = "Gagal, disapproval karena kepuasaan Anda dibawah 90%"

    return Response({"status": "{}".format(data),
                     "deskripsi": "TODO"
                     })
