import time
import numpy as np
import uvicorn
from fastapi import FastAPI, Response
from config import BASE_DATA_PATH, DEBUG, APP_MAIN_PORT
from tools.logging_util import setup_logger
import json
from fastapi.middleware.cors import CORSMiddleware
from models.required_function import OpinionExtractor
from validate_input import AspectAnalysis
from loco_nlp.preprocessing.language_detector import pure_en_detector

operation_logger = setup_logger('operation', path=f"{BASE_DATA_PATH}/logs")
classification_logger = setup_logger('classification', path=f"{BASE_DATA_PATH}/logs")

app = FastAPI()
ABOP_extractor = OpinionExtractor()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NumpySerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (
                np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32,
                np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


print("""-----------------------------------------------------
------ Application ready to USE ---------------------      
-----------------------------------------------------""")


@app.get("/")
def test():
    results = ["App is ready to use"]
    return {"status": "successful", "result": results}


@app.post("/test")
def test():
    results = ["App is ready to use"]
    return {"status": "successful", "result": results}


# AI RESPONSE
@app.post("/absa_opinion")
async def spell_checker(data: AspectAnalysis):
    try:
        start_time = time.time()
        text_input = data.text
        result = [{f"lang_{index}":pure_en_detector(text),f"text_{index}": ABOP_extractor.absa_model(text,pure_en_detector(text))} for index, text in enumerate(text_input)]
        final_result = {
            "status": "successful",
            "result": result,
            "time_ms": int((time.time() - start_time) * 1000)
        }

    except Exception as e:

        operation_logger.exception(f"{__name__}: Model failed to classify: Error: {str(e)}")

        return {
            "status": "error",
            "error": [str(e)]
        }

    if not DEBUG:
        classification_logger.warning(final_result)
    return Response(content=json.dumps(final_result, cls=NumpySerializer), media_type="application/json")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=APP_MAIN_PORT, log_level="info", reload=True)
