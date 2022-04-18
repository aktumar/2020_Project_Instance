# Test project, mobile application backend
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org) 
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://www.w3.org/html/)
[![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)](https://mariadb.org) 
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)


##### Request models :arrow_lower_right:

- Request from CLIENT (insert/select from DB)

##### Server :arrow_lower_right:

Response model:

```
return{
    'status': status.HTTP_200_OK,
    'dat': rq,
    'key': key
}

or: 

return {
    'status': status.HTTP_400_BAD_REQUEST,
    'error': 'Произошла внутренняя ошибка сервера. Попробуйте позже',
}
```

##### SQL (insert/select/update) :arrow_lower_right:

##### Response models :arrow_lower_right:

JSON response models in 

```
return {
	'dat': rq
}
```

![Image alt](https://github.com/aktumar/2020_Project_Instance/blob/master/example/image_of_client_page.png)
