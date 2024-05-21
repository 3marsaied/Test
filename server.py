from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis

app = FastAPI()

class PatientData(BaseModel):
    patient_id: str
    name: str
    heart_rate: int

# Redis Cloud connection details
redis_host = 'redis-11068.c325.us-east-1-4.ec2.redns.redis-cloud.com'
redis_port = 11068
redis_password = 'n8rNyzV1BBbA00Ki4kK92poJXxbSuOB5'

@app.post("/receive_data")
async def receive_data(patient_data: PatientData):
    try:
        # Connect to Redis Cloud
        r = redis.StrictRedis(
            host=redis_host, port=redis_port, password=redis_password
        )

        # Store data in Redis
        redis_key = f"patient:{patient_data.patient_id}"
        r.rpush(redis_key, patient_data.json())

        return {"message": "Data received and stored successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store data: {str(e)}")
