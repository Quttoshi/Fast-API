import httpx
from fastapi import APIRouter, HTTPException
from models import JokeResponse

router = APIRouter(prefix="/jokes", tags=["jokes"])

JOKES_API_URL = "https://official-joke-api.appspot.com/random_joke"

@router.get("/random", response_model=JokeResponse)
async def get_random_joke() -> JokeResponse:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(JOKES_API_URL)
            
            if response.status_code == 200:
                joke_data = response.json()
                return JokeResponse(**joke_data)
            else:
                raise HTTPException(
                    status_code=503,
                    detail=f"External API returned status {response.status_code}"
                )
    
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="External API timeout - took too long to respond"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to connect to external API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
