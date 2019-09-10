from django.db import models


# Create your models here.
class PengajuanKredit(models.Model):
    username = models.CharField(max_length=225)
    kepuasaan = models.IntegerField(max_length=225)
    jumlah_feedback = models.IntegerField(max_length=225)
    terakhir_online = models.DateField(max_length=225)
    bergabung = models.DateField(max_length=225)
    waktu_kirim_pesan = models.IntegerField(max_length=225)
    jumlah_pengikut = models.IntegerField(max_length=225)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username
