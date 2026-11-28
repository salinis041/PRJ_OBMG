from repository.care_team_repository import Add_CareTeam,get_CareTeam

def Add_CareTeamData(Uid, mrn, vist, task):
    Add_CareTeam(Uid, mrn, vist, task)
def get_CareTeam_MRN(vist):
    return get_CareTeam(vist)