def get_piece_membership(remaining_piece):
    degree={
        "small_amout_piece_remaining": 0,
        "moderate_amout_piece_remaining": 0,
        "large_amout_piece_remaining": 0
    }

    if remaining_piece>=0 and remaining_piece <=5:
        degree["small_amout_piece_remaining"]=1
        degree["moderate_amout_piece_remaining"]=0
        degree["large_amout_piece_remaining"]=0
    
    elif remaining_piece>=7 and remaining_piece <=10:
        degree["small_amout_piece_remaining"]=0
        degree["moderate_amout_piece_remaining"]=1
        degree["large_amout_piece_remaining"]=0
        
    elif remaining_piece>=12 and remaining_piece <=16:
        degree["small_amout_piece_remaining"]=0
        degree["moderate_amout_piece_remaining"]=0
        degree["large_amout_piece_remaining"]=1
        
    elif remaining_piece>5 and remaining_piece <7:
        degree["small_amout_piece_remaining"]=float((7-remaining_piece)*1.0/(7-5))
        degree["moderate_amout_piece_remaining"]=float((remaining_piece-5)*1.0/(7-5))
        degree["large_amout_piece_remaining"]=0
        
    elif remaining_piece>10 and remaining_piece <12:
        degree["small_amout_piece_remaining"]=0
        degree["moderate_amout_piece_remaining "]=float((12-remaining_piece)*1.0/(12-10))
        degree["large_amout_piece_remaining"]=float((remaining_piece-10)*1.0/(12-10))
    
    return degree

def get_moves_membership(moves):
    degree={
        "few": 0,
        "mid": 0,
        "huge": 0
    }

    if moves>=0 and moves <=70:
        degree["few"]=1
        degree["mid"]=0
        degree["huge"]=0
    
    elif moves>=80 and moves <=100:
        degree["few"]=0
        degree["mid"]=1
        degree["huge"]=0
        
    elif moves>150:
        degree["few"]=0
        degree["mid"]=0
        degree["huge"]=1
        
    elif moves>70 and moves <80:
        degree["few"]=float((80-moves)*1.0/(80-70))
        degree["mid"]=float((moves-70)*1.0/(80-70))
        degree["huge"]=0
        
    elif moves>100 and moves <150:
        degree["few"]=0
        degree["mid"]=float((150-moves)*1.0/(150-100))
        degree["huge"]=float((moves-100)*1.0/(150-100))

    return degree


def fuzzy_rules_evaluation(piece, moves):
    degree={
        "narrow": 0,
        "moderate": 0,
        "huge": 0
    }

    moderate1 = min(piece["small_amout_piece_remaining"], moves["few"])
    narrow1 = min(piece["small_amout_piece_remaining"], moves["mid"])
    narrow2 = min(piece["small_amout_piece_remaining"], moves["huge"])

    huge1 = min(piece["moderate_amout_piece_remaining"], moves["few"])
    moderate2 = min(piece["moderate_amout_piece_remaining"], moves["mid"])
    narrow3 = min(piece["moderate_amout_piece_remaining"], moves["huge"])

    huge2 = min(piece["large_amout_piece_remaining"], moves["few"])
    huge3 = min(piece["large_amout_piece_remaining"], moves["mid"])
    moderate3 = min(piece["large_amout_piece_remaining"], moves["huge"])

    degree["narrow"] = max(narrow1,max(narrow2,narrow3))
    degree["moderate"] = max(moderate1, max(moderate2 , moderate3))
    degree["huge"] = max(huge1, max(huge2,huge3))

    return degree

def defuzzyfication(b):
    sum = b["huge"]+b["narrow"]+b["moderate"]
    up = (b["narrow"]*10+b["moderate"]*20+b["huge"]*30)
    if(sum==0):
        return 0
    cog = (up*1.0)/sum
    return cog

def fuzzy(moves, remaining_piece):
    move_membership = get_moves_membership(moves)
    piece_membership = get_piece_membership(remaining_piece)
    fuzzy_rules = fuzzy_rules_evaluation(piece_membership, move_membership)
    cog_value = defuzzyfication(fuzzy_rules)
    #print(cog_value)
    return cog_value

#fuzzy(50,2)