# GeoSpatialTest

Small Python project demonstrating geospatial data processing using GeoPandas and Shapely. It utilizes OpenAI to extract parameters for geospatial search (search location, search radius and max number of results to be returned) from user input. User can either input just address (location), or use a natural language query. Default values are added to the search query, if missing, and maximum values are enforced in case the parameters entered exceed limits. Search location, search area (circle) and search results are visualised in Folium map.

## Features

- Natural-language and form-based geospatial search
- AI extraction of structured search parameters
- Pydantic validation
- OpenStreetMap-based geospatial search
- Distance-based ranking
- Interactive Folium visualization
- Search-radius visualization

## How It Works

Natural-language query
        ↓
OpenAI / LLM
        ↓
SearchRequest (Pydantic)
        ↓
Geospatial search
        ↓
Distance filtering and ranking
        ↓
Folium map + results


## Architecture

geospatialtest.py
src/
    ai.py
    geo.py
    ui.py

ai.py : extraction of search parameters from user query in Natural language and returning them via SearchRequest
geo.py: performs Geospatial search based on parameters retrieved in SearchRequest from ai.py
ui.py: UI related procedures, presentation of search results (list of objects retrieved, Folium map)


## Example

Example natural-language request:

"Find the 4 nearest gas stations within 10 km of Svatoplukova, Prague."

- The user query in natural language is passed to AI (ai.py)
- AI extracts the following parameters for geospatial search from the query:
    - location: Svatoplukova, Prague
        - validation is performed, empty strings are not allowed
    - limit: 4 
        - in case user query does not contain number of objects to be retrieved, default value is used: 3
        - in case user enters number higher than the maximum value (10), the maximum value is used
    - radius_km: 10
        - in case user query does not contain search radius, default value is used: 5.0
        - in case user enters number higher than the maximum value (50), the maximum value is used
- AI returns the search parameters as a SearchRequest data type
- geospatial search is executed (geo.py) using the search parameters received, all results are returned as a list
- returned list is sorted based on a distance from the search location (geo.py), 
  4 results nearest to the search location are returned as a list
- details of the 4 results returned are displayed in UI (ui.py)
- Folium map with the Search location, search radius circle and the 4 results is displayed (ui.py)

## Screenshots

GeoSpatialTest - Home screen
![GeoSpatialTest - Home screen](screenshots/GeoSpatialTest-01-home-screen.png?raw=true "GeoSpatialTest - Home screen")

## Technology Stack

- Python
- Streamlit
- OpenAI
- Pydantic
- OSMnx,
- GeoPandas
- Shapely
- pyproj
- Folium
- GeoPy

## Installation

git clone ...
python -m venv .venv
pip install -r requirements.txt

## Configuration

Explain OPENAI_API_KEY and .env.example.
Never include the actual key.

## Running the Application

streamlit run geospatialtest.py

## Current Scope / Future Development

Short description of what the application currently does
and possible extensions.

- FastAPI endpoint.
- LLM interface.
- Agentic workflow.
