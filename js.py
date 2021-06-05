def info(id, name, phone):
    """
    CLIENT: Show information to client
    /client/info/
    """
    return {
        "id": id,
        "name": name,
        "phone": phone,
    }


def team(name):
    """
    CLIENT: Show information about team
    /client/team/
    """
    return {
        "name": name
    }


def news(content, start_date, end_date):
    """
    CLIENT: Show news to CLIENT
    /client/news/
    """
    return {
        "content": content,
        "start_date": str(start_date),
        "end_date": str(end_date)
    }


def number(submitted, processed, completed):
    """
    CLIENT: Show number of processed, submitted, completed project to CLIENT
    /client/number/
    """
    return {
        "submitted": submitted,
        "processed": processed,
        "completed": completed,
    }


def request(id, nm, mid, dd, st, c_dt, dsc, com, adr):
    """
    CLIENT: Show information about project to CLIENT
    /client/request/
    """
    return {
        "id": id,
        "name": nm,
        "member_id": mid,
        "deadline": dd,
        "status": st,
        "created_date": c_dt,
        "description": dsc,
        "comment": com,
        "address": adr,
    }
