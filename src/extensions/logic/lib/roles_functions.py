VOICE_PERMITTED_ROLES_NAMES = ('Ponente', 'Admin')
BAN_HAMMER_PERMITTED_ROLES_NAMES = ('Junta', 'Admin')

def have_permitted_rol(autor_roles, permitted_roles):
    for autor_rol in autor_roles:
        if autor_rol.name in permitted_roles:
            return True
    return False


def str_permitted_roles_names(permitted_roles):
    return ' o '.join(permitted_roles)
