async def simplify(group_name):
    simplified = str(group_name).replace("-", "").capitalize()
    return simplified