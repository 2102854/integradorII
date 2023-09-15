import json

# Cria um retorno de dicionário de uma lista de objetos para retorno json
def dict_helper_list(objlist):
    result = [item.obj_to_dict() for item in objlist]
    return result

# Cria um retorno de dicionário de um objeto para retorno json
def dict_helper_obj(obj):
    result = json.JSONDecoder().decode(json.dumps(obj.obj_to_dict(), indent = 2))
    return result
