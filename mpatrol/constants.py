LEADER_LEVELS = {
    1:{'life':20, 'cp':5, 'exp_cost':0},
    2:{'life':30, 'cp':10, 'exp_cost':100},
    3:{'life':40, 'cp':20, 'exp_cost':200},
    4:{'life':50, 'cp':50, 'exp_cost':500},
    5:{'life':100, 'cp':100, 'exp_cost':1000},
    6:{'life':200, 'cp':200, 'exp_cost':2000},
    7:{'life':300, 'cp':300, 'exp_cost':3000},
    8:{'life':400, 'cp':400, 'exp_cost':4000},
    9:{'life':500, 'cp':500, 'exp_cost':5000},
    10:{'life':1000, 'cp':1000, 'exp_cost':10000},
    11:{'life':2000, 'cp':2000, 'exp_cost':20000},
    12:{'life':4000, 'cp':4000, 'exp_cost':40000},
    13:{'life':8000, 'cp':8000, 'exp_cost':80000},
    14:{'life':16000, 'cp':16000, 'exp_cost':160000},
    15:{'life':32000, 'cp':32000, 'exp_cost':320000}
    }

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
    }

def happiness_intensity_weight(happiness):
    bin_count = len(HAPPINESS_INTENSITY_WEIGHTS)
    happiness = max(0,min(1,happiness))
    return HAPPINESS_INTENSITY_WEIGHTS[int(happiness*bin_count)-1]