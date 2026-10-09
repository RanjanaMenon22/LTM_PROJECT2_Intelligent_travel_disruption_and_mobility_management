from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# =========================================================
# TravelIQ Imports
# =========================================================

from App.trip_orchestrator import TripOrchestrator
from retrieval.hotel_search import HybridHotelSearch
from retrieval.attraction_search import HybridAttractionSearch
from Integrations.weather_api import WeatherAPI
from Integrations.routing_api import RoutingAPI


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="TravelIQ API",
    description=(
        "AI-Powered Adaptive Travel Planning "
        "and Disruption Recovery Platform"
    ),
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Initialize Services
# =========================================================

orchestrator = TripOrchestrator()

hotel_search = HybridHotelSearch()

attraction_search = HybridAttractionSearch()

weather_api = WeatherAPI()

routing_api = RoutingAPI()


# =========================================================
# Request Models
# =========================================================

class TripRequest(BaseModel):

    city: str

    days: int = 3

    budget: float = 5000

    interests: List[str] = [
        "historical",
        "cultural"
    ]

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    flight_number: Optional[str] = None

    flight_date: Optional[str] = None


class HotelRequest(BaseModel):

    city: str

    budget: float = 5000

    min_rating: float = 0

    top_k: int = 5

    query: Optional[str] = None


class AttractionRequest(BaseModel):

    city: str

    interests: List[str] = [
        "historical",
        "cultural"
    ]

    min_rating: float = 0

    max_entry_fee: Optional[float] = None

    top_k: int = 10


class WeatherRequest(BaseModel):

    latitude: float

    longitude: float


class RouteRequest(BaseModel):

    start_latitude: float

    start_longitude: float

    end_latitude: float

    end_longitude: float


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "project": "TravelIQ",
        "description": (
            "AI-Powered Adaptive Travel Planning "
            "and Disruption Recovery Platform"
        ),
        "status": "running",
        "version": "1.0.0"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "TravelIQ API"
    }


# =========================================================
# PLAN TRIP
# =========================================================

@app.post("/plan-trip")
def plan_trip(request: TripRequest):

    try:

        result = orchestrator.plan_trip(
            city=request.city,
            days=request.days,
            budget=request.budget,
            interests=request.interests,
            latitude=request.latitude,
            longitude=request.longitude,
            flight_number=request.flight_number,
            flight_date=request.flight_date
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# HOTEL SEARCH
# =========================================================

@app.post("/hotels")
def hotels(request: HotelRequest):

    try:

        result = hotel_search.search(
            city=request.city,
            query=request.query,
            min_rating=request.min_rating,
            max_price=request.budget,
            top_k=request.top_k
        )

        return {
            "success": True,
            "count": len(result),
            "data": result.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# ATTRACTION SEARCH
# =========================================================

@app.post("/attractions")
def attractions(request: AttractionRequest):

    try:

        results = []

        for interest in request.interests:

            result = attraction_search.search(
                city=request.city,
                query=interest,
                min_rating=request.min_rating,
                max_entry_fee=request.max_entry_fee,
                top_k=request.top_k
            )

            results.extend(
                result.to_dict(
                    orient="records"
                )
            )

        # Remove duplicate attractions
        unique = {}

        for item in results:

            key = (
                item.get("name")
                or item.get("popular_destination")
            )

            if key:
                unique[key] = item

        final_results = list(unique.values())

        return {
            "success": True,
            "count": len(final_results),
            "data": final_results
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# WEATHER
# =========================================================

@app.post("/weather")
def weather(request: WeatherRequest):

    try:

        result = weather_api.get_weather(
            latitude=request.latitude,
            longitude=request.longitude
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# ROUTE
# =========================================================

@app.post("/route")
def route(request: RouteRequest):

    try:

        result = routing_api.get_route(
            start_latitude=request.start_latitude,
            start_longitude=request.start_longitude,
            end_latitude=request.end_latitude,
            end_longitude=request.end_longitude
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# RUN DIRECTLY
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )