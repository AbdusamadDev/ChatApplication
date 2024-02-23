def to_dict(query):
    record = vars(query)
    del record["_sa_instance_state"]
    return record


def to_cursed_dict(result):
    record = {}
    for column, value in enumerate(result):
        record[column] = value
    return record

