from pydantic import BaseModel


class auth(BaseModel):
    """
    CLIENT: Authorization
    /client/auth/
    """
    phone: str
    jwt: str


class info(BaseModel):
    """
    CLIENT: Show information to client
    /client/info/
    """
    id: int
    key: str


class new_info(BaseModel):
    """
    CLIENT: Insert information about members
    /client/info/upload/
    """
    name: str
    id: int
    phone: str
    key: str


class news(BaseModel):
    """
    CLIENT: Insert news in web-site
    /client/news/upload/
    """
    id: int
    start_date: str
    end_date: str
    content: str


class request(BaseModel):
    """
    CLIENT: Insert information about project
    /client/request/upload/
    """
    project_name: str
    last_name: str
    first_name: str
    deadline: str = None
    status: int
    description: str = None
    phone: str
    comment: str = None
    address: str

class rate(BaseModel):
    """
    CLIENT: Update RATE from CLIENT
    /client/get_rate/
    """
    project_id: int
    comment: str = None
    rate: int
