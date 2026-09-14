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
    location: str
    limit: int = Field(default=results_default, gt=0, le=results_max, description="How many gas stations to find - upper limit prevents app misusing.")
    radius_km: float = Field(default=distance_default, le=distance_max, description="in what distance from the location to search")

    

def parse_search_query(user_input: str) -> SearchRequest:
    prompt = f"""
    You are an AI agent specialized in extracting data from user requests for geospatial data searches.
    You have to extract the following fields from the user query, or use the default values, if not specified explicitly:
    - location (address of a point of search - geospatial point, in relation to wich a search in geospatial data is performed. This should typically be the only address mentioned in the request. Try to remove words like 'ulice' or 'street', so the result could be used for search directly.) 
    - limit (how many results will be returned - relates to the amount mentioned in the query. Should be in range of 1 to {results_max} to prevent excessive queries, the default value is {results_default}, if not specified otherwise by the user) 
    - radius_km (how far from the search center the search in geospatial data is performed - relates to the distance mentioned in the query. The value should be less or equal to {distance_max} km, to prevent excessive queries, the default value is {distance_default} km, if not specified otherwise by the user) 
    
    Provide results in the JSON format.

    User query:
    {user_input}
    """

    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / "secret-config" / ".env"
    #env_path = Path("Documents/GITHub/GeoSpatialTest/secret-config/.env")

    if env_path.exists():
        print("✅ File .env successfuly located.")
    else:
        print(f"❌ File NOT found on adress: {env_path.resolve()}")

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

        #st.write(f"""Performing search:\n\n
        #Location: {search_request.location} ({location_map_url})\n
        #Results to return (max {results_max}, default {results_default}): {search_request.limit}\n
        #Distance from Location (max {distance_max} km, default {distance_default} km): {search_request.radius_km} km\n
        #""")

        with st.expander("Search details"):
            st.write(f"Location: {search_request.location}")
            st.write(f"Results (max {results_max}, default {results_default}): {search_request.limit}")
            st.write(f"Radius (max {distance_max} km, default {distance_default} km): {search_request.radius_km} km")

        return search_request
    except Exception as e:
        print("Error parsing JSON: ", e)
        print("AI response: ", result_text)
        return None
    
