import os
from datetime import datetime

# Create your views here.
def get_upload_path(instance, filename):
  return os.path.join(
      'uploads', 'user_%d' % instance.user.id, '%s_%s' % (datetime.now().strftime('%d%b%Y_%H%M%S'), filename))
