from rest_framework import serializers
from results.models import DkResults, FdResults

class DkResultsSerializer(serializers.ModelSerializer):
  class Meta:
    model = DkResults
    fields = ('pk', 'user', 'sport', 'contest_type', 'date', 'time', 
        'single_entry', 'contest_name', 'points', 'entry_fee', 'winnings',
        'place', 'contest_entries', 'entry_num', 'your_num_entries',
        'opponent', 'prize_pool', 'winnings_tix')

class FdResultsSerializer(serializers.ModelSerializer):
  class Meta:
    model = FdResults
    fields = ('pk', 'user', 'sport', 'contest_type', 'date', 'time', 
        'single_entry', 'contest_name', 'points', 'entry_fee', 'winnings',
        'place', 'contest_entries', 'entry_num', 'your_num_entries',
        'opponent', 'prize_pool', 'entry_id', 'link')
