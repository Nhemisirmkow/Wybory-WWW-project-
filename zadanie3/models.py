from django.db import models


# Create your models here.


class Test(models.Model):
    nazwa = models.CharField(max_length=84)

    def __str__(self):
        return "%s" % (self.nazwa)


class Kandydat(models.Model):
    nazwa = models.CharField(max_length=84, primary_key=True)
    kolor = models.CharField(max_length=42)

    def __str__(self):
        return "%s (Kolor : %s)" % (self.nazwa, self.kolor)

    # def clean(self):
    #     if self.answer != "42":
    #         raise ValidationError("The only correct answer is 42!")


class Kandydat_Województwo(models.Model):
    województwo = models.CharField(max_length=42)
    nazwa = models.CharField(max_length=42)
    liczba_głosów = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('województwo', 'nazwa')

    def __str__(self):
        return "%s : %s" % (self.województwo, self.nazwa,)


class Kandydat_Okręg(models.Model):
    okręg = models.PositiveIntegerField()
    nazwa = models.CharField(max_length=42)
    liczba_głosów = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('okręg', 'nazwa')

    def __str__(self):
        return "%s : %s" % (self.okręg, self.nazwa,)


class Kandydat_Gmina(models.Model):
    gmina = models.PositiveIntegerField()
    nazwa = models.CharField(max_length=42)
    liczba_głosów = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('gmina', 'nazwa')

    def __str__(self):
        return "%s : %s" % (self.gmina, self.nazwa,)


class Gmina(models.Model):
    id_gminy = models.PositiveIntegerField(primary_key=True)
    kod_gminy = models.CharField(max_length=42)
    nazwa = models.CharField(max_length=100)
    liczba_obwodów = models.PositiveIntegerField(default=0)
    uprawnionych = models.PositiveIntegerField(default=0)
    kart_wydanych = models.PositiveIntegerField(default=0)
    głosów_oddanych = models.PositiveIntegerField(default=0)
    głosów_nieważnych = models.PositiveIntegerField(default=0)
    głosów_ważnych = models.PositiveIntegerField(default=0)
    okręg = models.PositiveIntegerField(default=0)
    class Meta:
        unique_together = ('kod_gminy', 'okręg')

    def __str__(self):
        return "%s" % (self.nazwa)


class Okręg(models.Model):
    numer = models.PositiveSmallIntegerField(primary_key=True)
    liczba_gmin = models.PositiveIntegerField(default=0)
    uprawnionych = models.PositiveIntegerField(default=0)
    kart_wydanych = models.PositiveIntegerField(default=0)
    głosów_oddanych = models.PositiveIntegerField(default=0)
    głosów_nieważnych = models.PositiveIntegerField(default=0)
    głosów_ważnych = models.PositiveIntegerField(default=0)
    województwo = models.CharField(max_length=42)

    def __str__(self):
        return "%s" % (self.numer)


class Województwo(models.Model):
    nazwa_skrót = models.CharField(max_length=42, primary_key=True)
    nazwa = models.CharField(max_length=42)
    liczba_okręgów = models.PositiveIntegerField(default=0)
    uprawnionych = models.PositiveIntegerField(default=0)
    kart_wydanych = models.PositiveIntegerField(default=0)
    głosów_oddanych = models.PositiveIntegerField(default=0)
    głosów_nieważnych = models.PositiveIntegerField(default=0)
    głosów_ważnych = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s" % (self.nazwa)