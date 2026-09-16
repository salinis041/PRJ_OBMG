from repository.patient_repository import get_coorpathome,get_patientVisit

def get_patCordinat_list():
    return get_coorpathome()
def get_patCordinat_Visit(visit_id):
    return get_patientVisit(visit_id)