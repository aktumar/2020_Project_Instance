# Test project, mobile application backend



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