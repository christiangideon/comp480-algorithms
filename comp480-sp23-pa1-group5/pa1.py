# Name: pa1.py
# Author(s): Samuel Cacnio, Christian Gideon
# Date: 15 February 2023
# Description: This file runs a modification of the basic Gale-Shapley algorithm by adding in three
# additions to the base algorithm:
# 1. Each hospital can have any number of positions, not necessarily all the same.
# 2. A hospital can find some students unacceptable, and a student can find some hospitals unacceptable.
# 3. There can be an unequal number of available positions and students.
def pos_avail(dictionary):
    """
    Checks if there is at least one hospital in the dictionary
    with an open position and has not yet proposed to all 
    viable students
    Parameters:
    dictionary - (dict) contains hospitals as keys and
        list of preferences and number of positions as values
    Returns:
    k - (int) key of first hospital with an open position
    """
    for k in list(dictionary.keys()):
        #check for open position
        hospital = dictionary[k]
        if hospital[1]>0 and len(hospital[0])>0:#checks if hospital has at least 1 position left and has students left to propose to
            return k
    return -1

def gale_shapley(filename):
    """
    Runs Gale-Shapley algorithm on input
    from file filename.  Format of input file
    given in problem statement.
    Returns a list containing hospitals assigned to each 
    student, or None if a student is not assigned to a hospital.
    """
    # prepare input file for algorithm
    f = open(filename)
    counts = f.readline().split()
    h_count = int(counts[0]) #num of hospitals
    s_count = int(counts[1]) #num of students

    # keeping track of number of positions per hospital
    h_pos = f.readline().split()
    for i in range(len(h_pos)):
        h_pos[i] = int(h_pos[i])
    
    # setting up hospital entries with preferences and open positions
    h_pref = {}
    for i in range(h_count):
        i_pref = f.readline().split()
        for j in range(len(i_pref)):
            i_pref[j] = int(i_pref[j])
        h_pref[i] = [i_pref, h_pos[i]]

    # setting up student entries with preferences and match status
    s_pref = {}
    matches = [] #list of students' hospital matches--OUTPUT
    for i in range(s_count):
        i_pref = f.readline().split()
        for j in range(len(i_pref)):
            i_pref[j] = int(i_pref[j])
        s_pref[i] = [i_pref, False]
        #develop list of students' hospital matches
        matches.append(None)

    f.close()

    #begin algorithm
    curr_hos = pos_avail(h_pref) #key of first hospital
    while (curr_hos!=-1):
        curr_prop = h_pref[curr_hos][0].pop(0) #retrieve 1st student in hospital's preference list; pop because hospital only proposes once per student
        if (s_pref[curr_prop][1]==False):#if student is free
            matches[curr_prop]=curr_hos
            s_pref[curr_prop][1]=True #student is now matched
            h_pref[curr_hos][1]-=1#close 1 position
        else:
            stu_curr_engage = s_pref[curr_prop][0].index(matches[curr_prop]) #get preference ranking of student's current match
            new_engage = s_pref[curr_prop][0].index(curr_hos) #get preference of current hospital in student's ranking
            if (new_engage != None) and new_engage<stu_curr_engage: #compare rankings
                #swap if hospital is better than student's current match
                h_pref[matches[curr_prop]][1]+=1 #open 1 position
                matches[curr_prop] = curr_hos #change assignment
                h_pref[curr_hos][1]-=1
            #else: student rejects this hospital
        curr_hos = pos_avail(h_pref) #find next hospital with open position
                
    return matches