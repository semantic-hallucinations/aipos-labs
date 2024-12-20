from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from crud import *  
from database import conn
from typing import Optional
from datetime import date
import logging
import os


app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))
logging.basicConfig(level=logging.DEBUG, filename="py_log.log",filemode="w")

@app.get("/", response_class=HTMLResponse)
def menu_page(request: Request):
    logging.debug("Opening menu window")
    return templates.TemplateResponse("menu.html", {"request": request})


@app.post("/owners/add")
def create_owner(contact: str = Form(...), type_of_owner: str = Form(...), name: str = Form(...), owners_fullname : str = Form(...)):
    try:
        add_owner(contact, type_of_owner, name, owners_fullname)
        logging.debug("Adding owner")
        return RedirectResponse(url="/owners/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while adding owner")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/objects/add")
def create_object(type: str = Form(...), adress: str = Form(...), name: str = Form(...), number_of_places: int = Form(...), owner_id: int = Form(...)):
    try:
        add_object(type, adress, name, number_of_places,owner_id)
        logging.debug("Adding object")
        return RedirectResponse(url="/objects/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while adding object")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/popularities/add")
def create_popularity(event_date: date = Form(...), number_of_visitors: int = Form(...), object_id: int = Form(...)):
    try:
        add_popularity(event_date, number_of_visitors, object_id)
        logging.debug("Adding popularity")
        return RedirectResponse(url="/popularities/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while adding popularity")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/events/add")
def create_event(fut_event_date: date = Form(...), event_name: str = Form(...), event_type: str = Form(...), object_id: int = Form(...)):
    try:
        add_event(fut_event_date, event_name, event_type, object_id)
        logging.debug("Adding event")
        return RedirectResponse(url="/events/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while adding event")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dates/add")
def create_date(opening_date: date = Form(...), closing_date: date = Form(...), object_id: int = Form(...)):
    try:
        add_date(opening_date, closing_date, object_id)
        logging.debug("Adding working dates")
        return RedirectResponse(url="/dates/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while adding working dates")
        raise HTTPException(status_code=500, detail=str(e))

# обновление
@app.get("/owners/put/{owner_id}")
def edit_owner_page(request: Request):
    owner_id = request.path_params['owner_id']
    owner = get_owner_by_id(owner_id)
    logging.debug("Owners editing window")
    if owner is None:
        logging.warning("Owner not found")
        raise HTTPException(status_code=404, detail="Owner not found")
    return templates.TemplateResponse("edit_owner.html", {"request": request, "owner": owner})

@app.post("/owners/put/{owner_id}")
def edit_owner(request: Request, contact: str = Form(...), type_of_owner: str = Form(...), name: str = Form(...), owners_fullname: str = Form(...)):
    try:
        owner_id = request.path_params['owner_id']
        update_owner(owner_id, contact, type_of_owner, name, owners_fullname)
        logging.debug("Update владельца")
        return RedirectResponse(url="/owners/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while editing owner")
        raise HTTPException(status_code=500, detail=str(e))

#----------------

@app.get("/objects/put/{object_id}")
def edit_object_page(request: Request):
    object_id = request.path_params['object_id']
    object = get_object_by_id(object_id)
    owners = get_owners()
    logging.debug("Objects editing window")
    if object is None:
        logging.warning("Object not found")
        raise HTTPException(status_code=404, detail="Object not found")
    return templates.TemplateResponse("edit_object.html", {"request": request, "object": object, "owners": owners})
    
@app.post("/objects/put/{object_id}")
def edit_object(request: Request, type: str = Form(...), adress: str = Form(...), name: str = Form(...), number_of_places: int = Form(...),owner_id: int = Form(...)):
    try:
        object_id = request.path_params['object_id']
        update_object(object_id, type, adress, name, number_of_places,owner_id)
        logging.debug("Update объекта")
        return RedirectResponse(url="/objects/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while editing object")
        raise HTTPException(status_code=500, detail=str(e))

#-------------    

@app.get("/popularities/put/{popularity_id}")
def edit_popularity_page(request: Request):
    popularity_id = request.path_params['popularity_id']
    popularity = get_popularity_by_id(popularity_id)
    logging.debug("Popilarytys editing window")
    if popularity is None:
        logging.warning("Popularity not found")
        raise HTTPException(status_code=404, detail="Popularity not found")
    return templates.TemplateResponse("edit_popularity.html", {"request": request, "popularity": popularity})

@app.post("/popularities/put/{popularity_id}")
def edit_popularity(request: Request, event_date: date = Form(...), number_of_visitors: int = Form(...)):
    try:
        popularity_id = request.path_params['popularity_id']
        update_popularity(popularity_id, event_date, number_of_visitors)
        logging.debug("Update популярности")
        return RedirectResponse(url="/popularities/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while editing popularity")
        raise HTTPException(status_code=500, detail=str(e))

#-------------------

@app.get("/events/put/{event_id}")
def edit_event_page(request: Request):
    event_id = request.path_params['event_id']
    event = get_event_by_id(event_id)
    logging.debug("Events editing window")
    if event is None:
        logging.warning("Event not found")
        raise HTTPException(status_code=404, detail="Event not found")
    return templates.TemplateResponse("edit_event.html", {"request": request, "event": event})

@app.post("/events/put/{event_id}")
def edit_event(request: Request, fut_event_date: date = Form(...), event_name: str = Form(...), event_type: str = Form(...)):
    try:
        event_id = request.path_params['event_id']
        update_event(event_id, fut_event_date, event_name, event_type)
        logging.debug("Update мероприятия")
        return RedirectResponse(url="/events/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while editing event")
        raise HTTPException(status_code=500, detail=str(e))

#---------------------

@app.get("/dates/put/{date_id}")
def edit_date_page(request: Request):
    date_id = request.path_params['date_id']
    date = get_date_by_id(date_id)
    logging.debug("Working dates editing window")
    if date is None:
        logging.warning("Date not found")
        raise HTTPException(status_code=404, detail="Date not found")
    return templates.TemplateResponse("edit_date.html", {"request": request, "date": date})

@app.post("/dates/put/{date_id}")
def edit_date(request: Request, opening_date: date = Form(...), closing_date: date = Form(...)):
    try:
        date_id = request.path_params['date_id']
        update_date(date_id, opening_date, closing_date)
        logging.debug("Update working dates")
        return RedirectResponse(url="/dates/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while editing working dates")
        raise HTTPException(status_code=500, detail=str(e))

# удаление 
@app.post("/owners/delete/{owner_id}")
def remove_owner(request: Request):
    try:
        owner_id = request.path_params['owner_id']
        delete_owner(owner_id)
        logging.debug("Delete owner")
        return RedirectResponse(url="/owners/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while deleting owner")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/objects/delete/{object_id}")
def remove_object(request: Request):
    try:
        object_id = request.path_params['object_id']
        delete_city_object(object_id)
        logging.debug("Delete object")
        return RedirectResponse(url="/objects/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while deleting object")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/popularities/delete/{popularity_id}")
def remove_popularity(request: Request):
    try:
        popularity_id = request.path_params['popularity_id']
        delete_popularity(popularity_id)
        logging.debug("Delete popularity")
        return RedirectResponse(url="/popularities/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while deleting popularity")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/events/delete/{event_id}")
def remove_event(request: Request):
    try:
        event_id = request.path_params['event_id']
        delete_event(event_id)
        logging.debug("Delete event")
        return RedirectResponse(url="/events/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while deleting event")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/dates/delete/{date_id}")
def remove_date(request: Request):
    try:
        date_id = request.path_params['date_id']
        delete_date(date_id)
        logging.debug("Delete working dates")
        return RedirectResponse(url="/dates/", status_code=303)
    except Exception as e:
        logging.warning("Something gone wrong while deleting working dates")
        raise HTTPException(status_code=500, detail=str(e))

#---особые--селекты-----
# @app.get("/objects/currrent")
# def view_current_objects(request: Request):
#     curr_objects = fetch_current_objects()
#     return templates.TemplateResponse("but_curr_object.html", {"request": request, "curr_objects": curr_objects})

# @app.get("/events/upcoming")
# def view_upcoming_events(request: Request):
#     upcoming_events = fetch_upcoming_events()
#     return templates.TemplateResponse("upcoming_events.html", {"request": request, "upcoming_events": upcoming_events})

# @app.get("/objects/select_type", response_class=HTMLResponse)
# def select_object_type_page(request: Request):
#     objects = list(set([i[2] for i in get_objects()]))
#     return templates.TemplateResponse(
#         "select_object_type.html", 
#         {"request": request, "objects": objects}
#     )


# @app.post("/objects/select_type", response_class=HTMLResponse)
# def view_objects_by_type(request: Request, type: str = Form(...)):
#     try:
#         logging.debug(type)
#         cur_type_objects = fetch_curr_type_objects(type) 
#         logging.debug(cur_type_objects)
#         return templates.TemplateResponse(
#             "but_curr_type_object.html", 
#             {"request": request, "cur_type_objects": cur_type_objects, "type": type}
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


#----обычные-----селекты----------
@app.get("/owners/", response_class=HTMLResponse)
def view_owners(request: Request):
    owners = get_owners() 
    return templates.TemplateResponse("view_owners.html", {"request": request, "owners": owners})

@app.get("/objects/", response_class=HTMLResponse)
def view_objects(request: Request):
    objects = get_objects() 
    owners = get_owners()
    return templates.TemplateResponse("view_objects.html", {"request": request, "objects": objects, "owners": owners})

@app.get("/popularities/", response_class=HTMLResponse)
def view_popularities(request: Request):
    popularities = get_popularities() 
    objects = get_objects() 
    return templates.TemplateResponse("view_popularities.html", {"request": request, "popularities": popularities, "objects": objects})

@app.get("/events/", response_class=HTMLResponse)
def view_events(request: Request):
    events = get_events() 
    objects = get_objects() 
    return templates.TemplateResponse("view_events.html", {"request": request, "events": events, "objects": objects})

@app.get("/dates/", response_class=HTMLResponse)
def view_dates(request: Request):
    dates = get_dates() 
    objects = get_objects() 
    return templates.TemplateResponse("view_dates.html", {"request": request, "dates": dates, "objects": objects})


@app.on_event("shutdown")
def shutdown_db_connection():
    conn.close()