# GeoSpatialTest

A small Python application demonstrating AI-assisted geospatial search using GeoPandas, Shapely and OpenStreetMap data.  
  
The application uses an OpenAI model to convert natural-language input into structured search parameters: location, search radius and maximum number of results. If the requested result count or search radius exceeds the configured maximum, the LLM is instructed to reduce it to the maximum allowed value. The resulting parameters are then validated by Pydantic before the geospatial search is executed.  

Users can either enter an address directly or describe the search in natural language. Results are ranked by distance and displayed both as a list and on an interactive Folium map, including the search location and search-radius boundary.  

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
        Structured parameters  
                ↓  
        SearchRequest (Pydantic validation)  
                ↓  
        Deterministic geospatial search  
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

**geospatialtest.py** — Main Streamlit application and workflow orchestration.  
**ai.py** — Converts natural-language input into a validated `SearchRequest`.  
**geo.py** — Performs geocoding, geospatial search, distance calculation, filtering and ranking.  
**ui.py** — Presents search results and builds the interactive Folium map.  

 
## Example

Example natural-language request:  

"Find the 4 nearest gas stations within 10 km of Svatoplukova, Prague."  

- The natural-language query is passed to the LLM (`ai.py`).
- The LLM extracts and normalizes the parameters required for the geospatial search:
    - `location`: `Svatoplukova, Prague`
        - Empty locations are rejected by validation.
    - `limit`: `4`
        - Default: `3`
        - Maximum: `10`
        - Values above the maximum are reduced to `10` by the LLM.
    - `radius_km`: `10`
        - Default: `5.0`
        - Maximum: `50`
        - Values above the maximum are reduced to `50` by the LLM.
- The structured parameters are parsed and validated as a Pydantic `SearchRequest`.
- The validated parameters are passed to the deterministic geospatial search (`geo.py`).
- Results are sorted by distance from the search location and limited to the requested number.
- Result details are displayed in the Streamlit UI (`ui.py`).
- The search location, search-radius boundary and returned petrol stations are displayed on an interactive Folium map (`ui.py`).

## Screenshots

![GeoSpatialTest - Home screen](screenshots/GeoSpatialTest-01-home-screen.png?raw=true "GeoSpatialTest - Home screen")  
Home screen  

![GeoSpatialTest - Home screen with search help expanded](screenshots/GeoSpatialTest-02-home-screen-search-instructions-expanded.png?raw=true "GeoSpatialTest - Home screen with search help expanded")  
Home screen with search help expanded  

![GeoSpatialTest - User query in natural language](screenshots/GeoSpatialTest-03-user-query-in-natural-language.png?raw=true "GeoSpatialTest - User query in natural language")  
User query in natural language  

![GeoSpatialTest - User query processed by AI - expanded section with search parameters](screenshots/GeoSpatialTest-04-expanded-section-with-search-query-details.png?raw=true "GeoSpatialTest - User query processed by AI - expanded section with search parameters")  
User query processed by AI - expanded section with search parameters  

![GeoSpatialTest - Search results in a list](screenshots/GeoSpatialTest-05-search-results-list.png?raw=true "GeoSpatialTest - Search results in a list")  
Search results in a list  

![GeoSpatialTest - Search results in a map](screenshots/GeoSpatialTest-06-search-results-map.png?raw=true "GeoSpatialTest - Search results in a map")  
Search results in a map  

![GeoSpatialTest - Search results in a map - detail of Search radius](screenshots/GeoSpatialTest-07-search-results-map-search-radius.png?raw=true "GeoSpatialTest - Search results in a map - detail of Search radius")  
Search results in a map - detail of Search radius  

![GeoSpatialTest - Search results in a map - detail of Search location](screenshots/GeoSpatialTest-08-search-results-map-search-location.png?raw=true "GeoSpatialTest - Search results in a map - detail of Search location")  
Search results in a map - detail of Search location  

![GeoSpatialTest - Search results in a map - detail of Search result](screenshots/GeoSpatialTest-09-search-results-map-search-result-detail.png?raw=true "GeoSpatialTest - Search results in a map - detail of Search result")  
Search results in a map - detail of Search result  


## Technology Stack

- **Python** — application language
- **Streamlit** — web UI
- **OpenAI API** — natural-language query interpretation
- **Pydantic** — structured data validation
- **OSMnx / OpenStreetMap** — geospatial data retrieval
- **GeoPandas / Shapely / pyproj** — geospatial processing
- **GeoPy** — geocoding and distance utilities
- **Folium** — interactive map visualization

## Installation

The following example uses Windows:  

        git clone https://github.com/Luke-75/GeoSpatialTest.git
        cd GeoSpatialTest

        python -m venv .venv
        .venv\Scripts\activate

        pip install -r requirements.txt 

## Configuration

### OpenAI API

The application requires an OpenAI API key.

- Create an API key in your OpenAI Platform account (https://platform.openai.com/api-keys).
- Create a `secret-config` directory in the project root.
- Copy `.env.example` to `secret-config/.env`.
- Add your API key to the `.env` file:

        OPENAI_API_KEY=your_openai_api_key_here

The `secret-config` directory is excluded from version control through `.gitignore`. Never commit API keys or other credentials to the repository.
        
### Nominatim User Agent

The application uses the Nominatim geocoding service. Configure a descriptive user-agent name in `secret-config/.env`:  

        NOMINATIM_USER_AGENT_NAME=your_application_name

## Running the Application

        streamlit run geospatialtest.py

## Current Scope / Future Development

The current application focuses on finding nearby petrol stations from either a direct location or a natural-language query.  

Possible future improvements include:  

- Generalizing the search from petrol stations to arbitrary points of interest
- Supporting more complex spatial queries and relationships
- Exposing geospatial search functionality through a FastAPI endpoint
- Adding automated unit and integration tests
- Extending the workflow toward agentic geospatial tasks
