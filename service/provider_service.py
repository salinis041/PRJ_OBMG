from repository.provider_repository import (insert_user,update_user,update_provider_new,
        get_Providerdetails,get_provider_by_id,update_provider,get_provider_AddList_id,Delete_PrAdd)


def register_user(data):
    Usr_id = int(data.get("usrid")or 0)
    if Usr_id ==0:
        print(Usr_id)
        insert_user(data)
    else:
        print(Usr_id)
        update_user(data)


    return ''
def get_provider_list(
    search=None):


    details = get_Providerdetails(
        search=search
    )
    # for x in details:
    #  print(x)
    return {
        "details": details,
        "search": search or ""
    }
def get_provider_list_UId(user_id):


    details = get_provider_by_id(
        user_id
    )

    return {
        "details": details
    }
def get_provider_Addlist_UId(user_id):
    AddList = get_provider_AddList_id(
        user_id
    )


    return {
        "AddList": AddList
    }
def addedit_provider(data,addresses):
    Prv_id = int(data.get("pid") or 0)
    if Prv_id ==0:
        update_provider(data, addresses)
    else:
        update_provider_new(data, addresses)



    return ''
def get_provider_list(
    search=None):


    details = get_Providerdetails(
        search=search
    )
    return {
        "details": details,
        "search": search or ""
    }
def delete_providerAddress(address_id):
    Delete_PrAdd(address_id)

    return True