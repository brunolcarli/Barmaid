

def condition(column, value, operator='='):
    return {'column': column, 'operator': operator, 'value': value}


def get_discord_id(server_id, author_id):
    return f'{server_id}:{author_id}'
