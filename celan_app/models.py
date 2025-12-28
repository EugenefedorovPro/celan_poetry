from django.db import models


class Collection(models.Model):
    name = models.CharField(max_length=255, default="")
    genre = models.CharField(max_length=255, default="")
    is_real_celan_collection = models.CharField(max_length = 255, default="")
    year_publication = models.PositiveIntegerField(null=True, blank=True)
    number_verses = models.PositiveBigIntegerField(default=0)
    notes = models.TextField(default="")

    def __str__(self):
        name = self.name if self.name else "no name"
        year = self.year_publication if self.year_publication else "no year"
        return f"{name} - {year}"


class Verse(models.Model):
    collection = models.ForeignKey("Collection", on_delete=models.PROTECT, null = True)
    title = models.CharField(max_length=255, default="")
    text = models.TextField(default="")

    def __str__(self):
        return self.title if self.title else self.text[:15]
