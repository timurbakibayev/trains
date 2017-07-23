from django.db import models

# Create your models here.
class Track(models.Model):
    length = models.DecimalField(default=1000, max_digits=7, decimal_places=2) #in meters
    name = models.TextField(default="Старт-Финиш")
    start_name = models.TextField(default="Старт")

    def __str__(self):
        return self.name + " (" + str(self.length) + " км.)"

class Switch(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    position = models.DecimalField(max_digits=7, decimal_places=2)
    name = models.TextField()
    number_of_tracks = models.IntegerField(default=1)
    trains_fit = models.IntegerField(default=1)
    is_start = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)
    mins_acc = models.IntegerField()
    mins_brk = models.IntegerField()
    mins_main = models.IntegerField()

    def __str__(self):
        return str(self.position) + ": " + self.name

    class Meta:
        ordering = ["position"]
        verbose_name_plural = "switches"
