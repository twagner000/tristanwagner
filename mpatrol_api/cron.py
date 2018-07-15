from django_cron import CronJobBase, Schedule

from . import models

class StructureInterestCronJob(CronJobBase):
    schedule = Schedule(run_every_mins=60)
    code = 'mpatrol_api.structure_interest'
    
    def do(self):
        pass
        #calc today_start
        #for each active games where last interest update < today_start (for school in School.objects.all():)
            #for each player filtered having interest building(s)
                #update gold
            #update game last interest update