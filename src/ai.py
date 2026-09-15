from pydantic import BaseModel, Field, field_validator
#from geo import geocode
#import openai
from openai import OpenAI
import json
from dotenv import load_dotenv
import os
from pathlib import Path
import streamlit as st

results_max = 10
results_default = 3
distance_max = 50.0
distance_default = 5.0

location_map_url = ""


class SearchRequest(BaseModel):
    location: str = Field(min_length=1, description="Location from which to search for nearby petrol stations.")
    limit: int = Field(default=results_default, gt=0, le=results_max, description="Maximum number of petrol stations to return.")
    radius_km: float = Field(default=distance_default, gt=0, le=distance_max, description="Search radius around the location, in kilometers.")
    @field_validator("location")
    @classmethod
    def validate_location(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Location must not be empty.")
        return value
    

def parse_search_query(user_input: str) -> SearchRequest:
    prompt = f"""
    You extract structured parameters from natural-language requests for geospatial searches.

    Extract the following fields:

    - location:
    The location used as the center of the geospatial search. Return only the address/location itself, without surrounding phrases such as "street", "ulice", "near", or "around".

    - limit:
    Number of results to return.
    Default: {results_default}
    Minimum: 1
    Maximum: {results_max}
    If the requested value exceeds the maximum, use {results_max}.

    - radius_km:
    Search radius in kilometers.
    Default: {distance_default}
    Must be greater than 0.
    Maximum: {distance_max}
    If the requested value exceeds the maximum, use {distance_max}.

    Return the extracted parameters as JSON.

    User query:
    {user_input}
    """

    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / "secret-config" / ".env"

    """
    if env_path.exists():
        print("✅ File .env successfuly located.")
    else:
        print(f"❌ File NOT found on adress: {env_path.resolve()}")
    """
    
    load_dotenv(dotenv_path=env_path)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")
    #print("API key: " + openai_api_key)

    oai_client = OpenAI(api_key=openai_api_key)

    response = oai_client.chat.completions.create(
        #model = "gpt-4",
        model = "gpt-3.5-turbo",
        messages = [{"role":"user", "content": prompt}],
        temperature = 0
    )

    result_text = response.choices[0].message.content.strip()

    # verify data conforms to valudation criteria, then convert JSON to Python data type and validate with Pydantic
    try:
        result_json = json.loads(result_text)

        search_request = SearchRequest(**result_json)

        # debug
        #st.write(search_request)

        with st.expander("Search details"):
            st.write(f"Location: {search_request.location}")
            st.write(f"Results (max {results_max}, default {results_default}): {search_request.limit}")
            st.write(f"Radius (max {distance_max} km, default {distance_default} km): {search_request.radius_km} km")

        return search_request
    except Exception as e:
        print("Error parsing JSON: ", e)
        print("AI response: ", result_text)
        return None
    
