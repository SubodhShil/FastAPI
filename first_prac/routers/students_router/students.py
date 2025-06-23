from fastapi import APIRouter
from typing import Union
from .db import user_list

router = APIRouter()

# Query parameter 

# 1
@router.get('/roll/')
async def roll(name: str | None = "Unknown", roll_no: int = 0):
    return {"name": name, "roll_no": roll_no}

# 2
@router.get('/gpa/')
async def gpa(gpa: float, name: Union[str, None] = "Random Student"):
    return {"name": name, "gpa": gpa}

# Practice Questions for Query Parameters:
# 1. Create an endpoint that filters students by minimum GPA
# 2. Create an endpoint that searches students by major
# 3. Create an endpoint that filters students by age range
# 4. Create an endpoint that searches students by hobby
# 5. Create an endpoint that sorts students by age or GPA

# Overall iteration
@router.get('/search/students/all')
async def search_for_all_students():
    return user_list


# Search each student by name
@router.get('/search/students/')
async def search_for_all_students(username:str):
    for user in user_list: 
        if username in user_list: 
            user_data = {}
            user_data["name"] = user
            for key, value in user_list[user].items():
                user_data[key] = value
            return user_data
        else:
            return {"error": "There is no such user found"}


# 1. Create an endpoint that filters students by minimum GPA
@router.get('/search/students/gpa')
async def search_by_gpa(min_gpa:float):
    # I will filter students got gpa above min_gpa
    filtered_students = {}
    for student in user_list:
        if user_list[student]["gpa"] > min_gpa:
            filtered_students[student] = user_list[student]

    return filtered_students


# 2. Create an endpoint that searches students by major
@router.get('/search/students/major')
async def search_by_major(major:str):
    filtered_students = {}
    for student in user_list:
        if user_list[student]['major'] == major:
            filtered_students[student] = user_list[student]

    return filtered_students


# 5. Create an endpoint that sorts students by age or GPA
@router.get('/search/students/sort/descending')
async def sort_by_gpa():
    sorted_students = {}
    sorted_students = sorted(user_list.items(), key=lambda x: x[1]['gpa'], reverse=True)
    return sorted_students


# 6. Create an endpoint that sorts students by age or GPA in descending order
@router.get('/search/students/sort/ascending')
async def sort_by_gpa():
    sorted_students = {}
    sorted_students = sorted(user_list.items(), key=lambda x: x[1]['gpa'], reverse=False)
    return sorted_students 