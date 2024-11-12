from fastapi import FastAPI, HTTPException, UploadFile, status, Form
import uvicorn
import pytesseract
from PIL import Image
from datetime import datetime
from io import BytesIO
import re
app = FastAPI()

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

@app.get("/")
async def root():
    return {"message": "Hello World"}

# api endpoint to input an image file and check date of birth > 21 using pyteseract
@app.post("/check_dob/")
async def check_dob(file: UploadFile = Form(...)):
    try:
        # Read the image data into a BytesIO object
        content = await file.read()
        image = Image.open(BytesIO(content))
        
        # Use pytesseract to read text directly from the BytesIO object
        text = pytesseract.image_to_string(image)
        
        # check if the text contains date of birth
        dates = re.findall(r'\d{2}[-/]\d{2}[-/]\d{4}', text)
        print(dates)
        # Convert the string dates to datetime objects
        date_objects = [datetime.strptime(date, '%m/%d/%Y') if '/' in date else datetime.strptime(date, '%d-%m-%Y') for date in dates]

        oldest_date = min(date_objects)
        if oldest_date:
            return {"message": f"Date of Birth: {oldest_date}"}
        else:
            return {"message": "Date of Birth not found in the image."}
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}


if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)