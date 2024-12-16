from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx
import logging
import requests
from datetime import date


BACKEND_URL = "http://lab7_api:8000"

app = FastAPI()
templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.DEBUG, filename="py_log.log",filemode="w")


@app.get("/", response_class=HTMLResponse)
def menu_page(request: Request):
    logging.debug("Opening menu window")
    return templates.TemplateResponse("menu.html", {"request": request})


@app.post("/owners/add", response_class=HTMLResponse)
async def create_owner(
    request: Request, 
    contact: str = Form(...), 
    type_of_owner: str = Form(...), 
    name: str = Form(...), 
    owners_fullname: str = Form(...)
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/owners/add", 
                json={
                    "contact": contact,
                    "type_of_owner": type_of_owner,
                    "name": name,
                    "owners_fullname": owners_fullname
                }
            )

        if response.status_code == 200:
            return RedirectResponse(url="/owners/", status_code=303)
        else:
            logging.warning(f"Error from API: {response.json()}")
            return templates.TemplateResponse("error.html", {"request": request, "error": response.json()})

    except Exception as e:
        logging.warning(f"Error while calling API: {str(e)}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@app.post("/objects/add", response_class=HTMLResponse)
async def create_object_web(
    request: Request, 
    type: str = Form(...), 
    adress: str = Form(...), 
    name: str = Form(...), 
    number_of_places: int = Form(...), 
    owner_id: int = Form(...)
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/objects/add", 
                json={
                    "type": type,
                    "adress": adress,
                    "name": name,
                    "number_of_places": number_of_places,
                    "owner_id": owner_id
                }
            )

        if response.status_code == 200:
            return RedirectResponse(url="/objects/", status_code=303)
        else:
            logging.warning(f"Error from API: {response.json()}")
            return templates.TemplateResponse("error.html", {"request": request, "error": response.json()})

    except Exception as e:
        logging.warning(f"Error while calling API: {str(e)}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@app.post("/events/add", response_class=HTMLResponse)
async def create_event_web(
    request: Request, 
    fut_event_date: str = Form(...), 
    event_name: str = Form(...), 
    event_type: str = Form(...), 
    object_id: int = Form(...)
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/events/add", 
                json={
                    "fut_event_date": fut_event_date,
                    "event_name": event_name,
                    "event_type": event_type,
                    "object_id": object_id
                }
            )

        if response.status_code == 200:
            return RedirectResponse(url="/events/", status_code=303)
        else:
            logging.warning(f"Error from API: {response.json()}")
            return templates.TemplateResponse("error.html", {"request": request, "error": response.json()})

    except Exception as e:
        logging.warning(f"Error while calling API: {str(e)}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@app.post("/dates/add", response_class=HTMLResponse)
async def create_date_web(
    request: Request, 
    opening_date: str = Form(...), 
    closing_date: str = Form(...), 
    object_id: int = Form(...)
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/dates/add", 
                json={
                    "opening_date": str(opening_date),
                    "closing_date": str(closing_date),
                    "object_id": object_id
                }
            )

        if response.status_code == 200:
            return RedirectResponse(url="/dates/", status_code=303)
        else:
            logging.warning(f"Error from API: {response.json()}")
            return templates.TemplateResponse("error.html", {"request": request, "error": response.json()})

    except Exception as e:
        logging.warning(f"Error while calling API: {str(e)}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


async def get_owner_from_api(owner_id: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/owner_by_id/", params={"owner_id": owner_id})
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Owner not found")
    except httpx.RequestError as e:
        logging.error(f"Request error: {e}")
        raise HTTPException(status_code=500, detail="Error while fetching data")

@app.get("/owners/put/{owner_id}", response_class=HTMLResponse)
async def edit_owner_page(request: Request, owner_id: int):
    owner = await get_owner_from_api(owner_id)
    return templates.TemplateResponse("edit_owner.html", {"request": request, "owner": owner})


@app.post("/owners/put/{owner_id}")
async def edit_owner(owner_id: int, contact: str = Form(...), type_of_owner: str = Form(...), name: str = Form(...), owners_fullname: str = Form(...)):
    try:
        owner_data = {
            "contact": contact,
            "type_of_owner": type_of_owner,
            "name": name,
            "owners_fullname": owners_fullname
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/owners/put/{owner_id}",
                json=owner_data
            )
            response.raise_for_status()

        logging.debug("Owner updated successfully")
        return RedirectResponse(url=f"/owners/", status_code=303)
    except httpx.HTTPStatusError:
        logging.warning("Error updating owner")
        raise HTTPException(status_code=500, detail="Error while updating owner")


async def delete_owner_from_api(owner_id: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{BACKEND_URL}/owners/delete/{owner_id}")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Error while deleting owner: {e}")
        raise HTTPException(status_code=500, detail="Error while deleting owner")
    except httpx.RequestError as e:
        logging.error(f"Request error: {e}")
        raise HTTPException(status_code=500, detail="Error while making request to API")

@app.post("/owners/delete/{owner_id}")
async def remove_owner(request: Request, owner_id: int):
    try:
        owner_id = request.path_params['owner_id']
        await delete_owner_from_api(owner_id)
        logging.debug(f"Owner {owner_id} deleted successfully")
        return RedirectResponse(url="/owners/", status_code=303)
    except HTTPException as e:
        logging.warning(f"Error while deleting owner {owner_id}: {e.detail}")
        raise e



@app.get("/owners/", response_class=HTMLResponse)
def view_owners(request: Request):
    try:
        response = requests.get(f"{BACKEND_URL}/owners/")
        response.raise_for_status()
        owners = response.json()
        return templates.TemplateResponse("view_owners.html", {"request": request, "owners": owners})
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to fetch owners")


@app.get("/objects/", response_class=HTMLResponse)
def view_objects(request: Request):
    try:
        response_objects = requests.get(f"{BACKEND_URL}/objects/")
        response_objects.raise_for_status()
        objects = response_objects.json()

        response_owners = requests.get(f"{BACKEND_URL}/owners/")
        response_owners.raise_for_status()
        owners = response_owners.json()

        return templates.TemplateResponse("view_objects.html", {"request": request, "objects": objects, "owners": owners})
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to fetch objects or owners")


@app.get("/popularities/", response_class=HTMLResponse)
def view_popularities(request: Request):
    try:
        response_popularities = requests.get(f"{BACKEND_URL}/popularities/")
        response_popularities.raise_for_status()
        popularities = response_popularities.json()

        response_objects = requests.get(f"{BACKEND_URL}/objects/")
        response_objects.raise_for_status()
        objects = response_objects.json()

        return templates.TemplateResponse("view_popularities.html", {"request": request, "popularities": popularities, "objects": objects})
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to fetch popularities or objects")


@app.get("/events/", response_class=HTMLResponse)
def view_events(request: Request):
    try:
        response_events = requests.get(f"{BACKEND_URL}/events/")
        response_events.raise_for_status()
        events = response_events.json()

        response_objects = requests.get(f"{BACKEND_URL}/objects/")
        response_objects.raise_for_status()
        objects = response_objects.json()

        return templates.TemplateResponse("view_events.html", {"request": request, "events": events, "objects": objects})
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to fetch events or objects")


@app.get("/dates/", response_class=HTMLResponse)
def view_dates(request: Request):
    try:
        response_dates = requests.get(f"{BACKEND_URL}/dates/")
        response_dates.raise_for_status()
        dates = response_dates.json()

        response_objects = requests.get(f"{BACKEND_URL}/objects/")
        response_objects.raise_for_status()
        objects = response_objects.json()

        return templates.TemplateResponse("view_dates.html", {"request": request, "dates": dates, "objects": objects})
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to fetch dates or objects")


