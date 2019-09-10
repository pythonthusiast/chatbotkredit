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
            response = BeautifulSoup(response.text)
            #cari table data
            tab = response.find("table", {"class": "c-table c-table--equal c-table--tight"})
            data = tab





    return Response({"status": "{}".format(data),
                     "deskripsi": "TODO"
                     })