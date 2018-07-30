import datetime
from pytz import timezone


pacific = timezone('US/Pacific')
months = {0:'January',1:'March',2:'May',3:'July',4:'September',5:'November'}

MAX_BATTALION_LEVEL = 15
BATTALION_TRAINING_XP_COST = 10

refresh_score_timedelta = datetime.timedelta(minutes=1)

