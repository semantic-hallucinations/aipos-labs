from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from crud import *  
from database import conn
from typing import Optional
from datetime import date
from pydantic import BaseModel
import logging
import os

app = FastAPI()
logging.basicConfig(level=logging.DEBUG, filename="py_log.log",filemode="w")


class Owner(BaseModel):
    contact: str
    type_of_owner: str
    name: str
    owners_fullname: str
    
class Object(BaseModel):
    type: str
    adress: str
    name: str
    number_of_places: int
    owner_id: int

class Popularity(BaseModel):
    event_date: date
    number_of_visitors: int
    object_id: int
    
class Event(BaseModel):
    fut_event_date: date
    event_name: str
    event_type: str
    object_id: int
    
class Date(BaseModel):
    opening_date: date
    closing_date: date
    object_id: int
    

@app.post("/owners/add", response_model=dict)
async def create_owner(owner: Owner):
    try:
        add_owner(owner.contact, owner.type_of_owner, owner.name, owner.owners_fullname)
        logging.debug("Adding owner via API")
        return {"status": "success", "message": "Owner added successfully"}
    except Exception as e:
        logging.warning("Something went wrong while adding owner via API")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/objects/add", response_model=dict)
async def create_object(owner: Object):
    try:
        add_object(owner.type, owner.adress, owner.name, owner.number_of_places, owner.owner_id)
        logging.debug("Adding object via API")
        return {"status": "success", "message": "Object added successfully"}
    except Exception as e:
        logging.warning("Something went wrong while adding object via API")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/popularities/add", response_model=dict)
async def create_popularity(popularity: Popularity):
    try:
        add_popularity(popularity.event_date, popularity.number_of_visitors, popularity.object_id)
        logging.debug("Adding popularity via API")
        return {"status": "success", "message": "Popularity added successfully"}
    except Exception as e:
        logging.warning("Something went wrong while adding popularity via API")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/events/add")
async def create_event(event: Event):
    try:
        add_event(event.fut_event_date, event.event_name, event.event_type, event.object_id)
        logging.debug("Adding event")
        return {"message": "Event added successfully"}
    except Exception as e:
        logging.warning("Something gone wrong while adding event")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/dates/add", response_model=dict)
async def create_date(date_request: Date):
    try:
        add_date(date_request.opening_date, date_request.closing_date, date_request.object_id)
        logging.debug("Adding working dates via API")
        return {"status": "success", "message": "Working dates added successfully"}
    except Exception as e:
        logging.warning("Something went wrong while adding working dates via API")
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/owners/put/{owner_id}", response_model=dict)
def edit_owner(owner_id: int, owner: Owner):
    try:
        update_owner(owner_id, owner.contact, owner.type_of_owner, owner.name, owner.owners_fullname)
        logging.debug("Owner updated via API")
        return {"status": "success", "message": "Owner updated successfully"}
    except Exception as e:
        logging.warning(f"Error while updating owner via API: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/owners/delete/{owner_id}")
def remove_owner(owner_id: int):
    try:
        delete_owner(owner_id)
        logging.debug(f"Owner {owner_id} deleted successfully")
        return {"status": "success", "message": f"Owner {owner_id} deleted successfully"}
    except Exception as e:
        logging.warning(f"Error while deleting owner {owner_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error while deleting owner")

@app.get("/owners/")
def owners():
    return get_owners()

@app.get("/owner_by_id/")
def owners(owner_id: int):
    owner = get_owner_by_id(owner_id)
    return owner

@app.get("/objects/")
def objects():
    return get_objects()

@app.get("/popularities/")
def popularities():
    return get_popularities()

@app.get("/events/")
def events():
    return get_events()

@app.get("/dates/")
def dates():
    return get_dates()
