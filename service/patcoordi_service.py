from repository.provider_repository import(get_specialty_list)
from repository.patient_repository import (get_coorpathome,get_patientVisit
,get_patVisitDetails,get_EncTask_list,get_EncTask_count,get_EnTaskVIdList
,get_EnTaskList_TId,update_ETask,Schedule_ETask,SchAppoimnt_ETask,ConfirmApoimnt_ETask
,get_Task_CmntList_Vistid)


def get_patCordinat_list():
    return get_coorpathome()
def get_patCordinat_Visit(visit_id):
    return get_patientVisit(visit_id)
def get_patVisit(visit_id):
    return get_patVisitDetails(visit_id)
def get_user_list():
    return get_specialty_list()
def get_EnTask_list_VId(mrn,vist):
    return get_EncTask_list(mrn,vist)
def get_EnTaskCont_VId(vist):
    return get_EncTask_count(vist)
def get_EnTaskVId(vist):
    return get_EnTaskVIdList(vist)
def get_EnTask_list_TId(TId):
    return get_EnTaskList_TId(TId)
def addedit_ETask(data,commentData):
    Dispo = data.get("disposition")
    details=''
    if Dispo == "Unable to Assist" or Dispo == "Unable to Reach-No SMS":
        details =update_ETask(data,commentData)
    elif (Dispo == "Scheduling Needed-PCP" or Dispo == "Scheduling Needed-Specialist"
          or Dispo == "Scheduling Needed-PCP & Specialist"
          or Dispo == "Scheduling Needed-PCP & 2 Specialist"):
        details = Schedule_ETask(data,commentData)
    elif Dispo == "Appointment Scheduled":
        details = SchAppoimnt_ETask(data,commentData)
    elif (Dispo == "Confirmed Attended" or Dispo == "Confirmed Did not Show"
          or Dispo == "Confirmed Canceled"
          or Dispo == "Confirmed Canceled and Rescheduled" or Dispo == "Unable to Confirm"
          or Dispo == "Scheduling Completed by Other" or Dispo == "Unable to schedule-Patient Barrier"
          or Dispo == "Unable to schedule-Office Barrier" or Dispo == "Unable to schedule-Payer Barrier"
          or Dispo == "Appointment Not Needed Any more" or Dispo == "Office Managed Appointment"
          or Dispo == "Archive Task"):
        details = ConfirmApoimnt_ETask(data,commentData)
    return details
def get_EnTaskCmnt_VstId(vist):
    CmntList = get_Task_CmntList_Vistid(
        vist
    )

    return  CmntList

