from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

import mysql.connector
from mysql.connector import errorcode

# Kết nối đến cơ sở dữ liệu MySQL
db = mysql.connector.connect(user='root', password='1412003@', host='localhost', database='new_database_3')

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home(request: Request):
    try:
        # Truy vấn dữ liệu từ cơ sở dữ liệu
        with db.cursor() as mycursor:
            query = "SELECT id, Name, Position, Office FROM data1"
            mycursor.execute(query)
            result = mycursor.fetchall()
    except mysql.connector.Error as e:
        # Xử lý lỗi kết nối hoặc truy vấn dữ liệu
        result = None

    # Hiển thị trang chủ và truyền dữ liệu vào template
    return templates.TemplateResponse("index.html", {"request": request, "data": result})

@app.post("/addnew")
async def add(request: Request,  name: str = Form(...), position: str = Form(...), office: str = Form(...)):
    message = ""
    try:
        # Thêm dữ liệu vào cơ sở dữ liệu
        with db.cursor() as mycursor:
            insert_code = "INSERT INTO `new_database_3`.`data1`  (Name, Position, Office) VALUES ( %s, %s, %s)"
            data = (name, position, office)
            mycursor.execute(insert_code, data)
            db.commit()
            message = "Dữ liệu đã được thêm vào bảng 'data1' trong cơ sở dữ liệu thành công!"
            
            # Truy vấn dữ liệu mới sau khi thêm và trả về dưới dạng JSON
            mycursor.execute("SELECT ID, Name, Position, Office FROM data1")
            result = mycursor.fetchall()
            return JSONResponse(content={"data": result})
    except mysql.connector.Error as e:
        # Xử lý lỗi khi thêm dữ liệu
        message = f"Lỗi khi thêm dữ liệu vào bảng: {str(e)}"
    except Exception as e:
        # Xử lý các lỗi khác
        message = f"Lỗi không xác định: {str(e)}"

    # Nếu có lỗi xảy ra, trả về thông báo lỗi
    return JSONResponse(content={"error": message}, status_code=500)

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
