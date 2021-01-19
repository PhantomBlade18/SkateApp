from mainapp.models import Rating,Location,Member
from django_pandas.io import read_frame

locs = Location.objects.all()
df = read_frame(locs)
df.head()