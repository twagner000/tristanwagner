INTEREST_RATES = {
    'private':.0875,
    'wb':.0715,
    'wbsap':.0715,
    }

MAX_SERVICE_FUNDING = {
    'health':450*10**6,
    'education':400*10**6,
    'security':900*10**6,
    }

PESTICIDE_CHOICES = (
    (0,'None'),
    (1,'Cheap'),
    (2,'Expensive'),
    )

PESTICIDES = [
    {'unhappiness':0, 'prod_loss':0},
    {'unhappiness':20, 'prod_loss':.04},
    {'unhappiness':5, 'prod_loss':.02}
    ]

CROPS = {
    'corn':{
        'planting_cost':100,
        'labor_cost':125,
        'other_cost':25,
        'pesticides':[
            {'cost':0,'yield':1500},
            {'cost':350,'yield':5000},
            {'cost':550,'yield':6000}
            ],
        'prices':[
            0.110,0.106,0.100,0.108,0.102,0.110,0.108,0.108,0.106,0.108,
            0.108,0.108,0.110,0.108,0.106,0.108,0.102,0.110,0.102,0.106,
            0.106,0.102,0.104,0.102,0.110,0.106,0.110,0.106,0.106,0.104,
            0.100,0.104,0.100,0.108,0.100,0.102,0.108,0.106,0.106,0.110,
            0.102,0.104,0.108,0.108,0.108,0.102,0.104,0.106,0.108,0.108,
            0.100,0.104,0.106,0.102,0.106,0.104,0.108,0.100,0.106,0.102,
            0.102,0.106,0.102,0.102,0.104,0.100,0.100,0.100,0.106,0.106,
            0.110,0.108,0.106,0.102,0.106,0.110,0.102,0.106,0.104,0.110,
            0.110,0.102,0.110,0.104,0.100,0.100,0.104,0.108,0.102,0.100,
            0.106,0.100,0.102,0.108,0.102,0.102,0.104,0.110,0.110,0.110,0.105
            ]
        },
    'cocoa':{
        'planting_cost':500,
        'labor_cost':175,
        'other_cost':175,
        'pesticides':[
            {'cost':0,'yield':500},
            {'cost':350,'yield':850},
            {'cost':450,'yield':1000}
            ],
        'prices':[
            3.85,3.41,3.30,2.64,2.09,2.42,2.20,2.09,1.98,1.54,1.32,1.21,
            1.27,1.21,1.14,1.07,1.06,1.06,1.07,1.10,1.04,0.96,0.91,0.95,
            0.95,1.03,1.06,1.05,1.11,1.08,1.03,1.02,0.94,0.94,0.94,0.91,
            0.99,1.07,1.11,1.17,1.11,1.03,0.96,0.92,0.94,0.94,0.90,0.94,
            1.01,0.99,0.91,0.95,0.97,1.05,1.04,1.00,1.08,1.00,1.07,1.10,
            1.17,1.22,1.22,1.14,1.20,1.21,1.17,1.09,1.07,1.07,1.07,1.06,
            1.10,1.04,1.10,1.05,0.99,1.04,1.08,1.08,1.15,1.18,1.12,1.19,
            1.19,1.26,1.26,1.20,1.25,1.27,1.27,1.21,1.28,1.29,1.29,1.21,
            1.23,1.18,1.11,1.12,1.10
            ]
        }
    }
        
POPULATION_BY_CLASS = {
    'l':4950000,
    'u':50000
    }

#represents bins from 0% to 100%; extremes get heavier weighting
HAPPINESS_INTENSITY_WEIGHTS = [3,2.4,1.9,1.6,1.4,1.2,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.5,1.6,1.7,1.85,2]

def happiness_intensity_weight(happiness):
    bin_count = len(HAPPINESS_INTENSITY_WEIGHTS)
    happiness = max(0,min(1,happiness))
    return HAPPINESS_INTENSITY_WEIGHTS[int(happiness*bin_count)-1]

#weightings for general happiness by socioeconomic class  
GENERAL_HAPPINESS_WEIGHTS_BY_CLASS = {
    'l':{
        'lfood':.2,
        'llux':.15,
        'ltax':.16,
        'health':.14,
        'education':.14,
        'security':.14,
        'env':.07
        },
    'u':{
        'ufood':.06,
        'ulux':.25,
        'utax':.22,
        'health':.1,
        'education':.1,
        'security':.24,
        'env':.03
        }
    }