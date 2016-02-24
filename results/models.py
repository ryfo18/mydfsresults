from django.db import models
from django.conf import settings


from results.utils import get_upload_path

class ResultsFiles(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  upload_date = models.DateTimeField(auto_now_add=True)
  file = models.FileField(upload_to=get_upload_path)

class Results(models.Model):
  CONTEST_TYPES = (
      ('50/50', 'Double-Up (50/50)'),
      ('H2H', 'Head-to-Head'),
      ('3X', 'Triple-Up'),
      ('5X', 'Quintuple-Up'),
      ('10X', '10x Multiplier'),
      ('WTA', 'Winner Take All'),
      ('LG', 'League'),
      ('SAT', 'Satellite/Qualifer'),
      ('QUA', 'Qualifer'),
      ('GPP', 'Guaranteed Prize Pool'),
      ('FRE', 'Freeroll'),
      ('PRI', 'Private'),
      ('NA', 'Unknown'),
  )
  SITES = (
      ('DK', 'DraftKings'),
      ('FD', 'FanDuel'),
  )
  SPORTS = (
      ('NFL', 'National Football League'),
      ('CFB', 'College Football'),
      ('NBA', 'National Basketball Association'),
      ('CBB', 'College Basketball'),
      ('NHL', 'National Hockey League'),
      ('MMA', 'Mixed Martial Arts'),
      ('MLB', 'Major League Baseball'),
      ('SOC', 'Soccer'),
      ('PGA', 'Golf'),
      ('LOL', 'eSports'),
      ('NAS', 'Nascar'),
  )
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  site = models.CharField(max_length=2, choices=SITES)
  sport = models.CharField(max_length=3, choices=SPORTS)
  contest_type = models.CharField(max_length=3, choices=CONTEST_TYPES)
  date = models.DateField('contest date')
  time = models.TimeField('contest time', default='00:00')
  single_entry = models.BooleanField(default=False)
  original_contest_name = models.CharField(max_length=128)
  contest_name = models.CharField(max_length=128)
  points = models.DecimalField(max_digits=5, decimal_places=2)
  entry_fee = models.DecimalField(max_digits=7, decimal_places=2)
  winnings = models.DecimalField(max_digits=10, decimal_places=2)
  place = models.IntegerField(default=0)
  contest_entries = models.IntegerField(default=1)
  entry_num = models.IntegerField(default=1)
  your_num_entries = models.IntegerField(default=0)
  opponent = models.CharField(max_length=30, null=True)
  prize_pool = models.DecimalField(max_digits=10, decimal_places=2)

class DkResults(Results):
  winnings_tix = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class FdResults(Results):
  entry_id = models.CharField(max_length=11)
  link = models.URLField()
