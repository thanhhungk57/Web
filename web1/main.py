from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException

import mysql.connector
from mysql.connector import errorcode

db = mysql.connector.connect(user ='root',password= '1412003@', host='localhost', database= 'new_database_3' )


templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home(request: Request):
    # Hiển thị trang chủ
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add")
async def add(request: Request, id: int = Form(...), name: str = Form(...), position: str = Form(...), office: str = Form(...)):
    message = ""
    try:
        # Kết nối đến cơ sở dữ liệu MySQL
        with mysql.connector.connect(user='root', password='1412003@', host='localhost', database='new_database_3') as db:
            # Tạo con trỏ
            with db.cursor() as mycursor:
                # Thêm dữ liệu vào bảng 'data1' trong cơ sở dữ liệu
                insert_code = "INSERT INTO `new_database_3`.`data1`  (id, Name, Position, Office) VALUES (%s, %s, %s, %s)"
                data = (id, name, position, office)
                mycursor.execute(insert_code, data)
                db.commit()
                message = "Dữ liệu đã được thêm vào bảng 'data1' trong cơ sở dữ liệu thành công!"
    except mysql.connector.Error as e:
        # Xử lý lỗi kết nối hoặc thêm dữ liệu
        message = f"Lỗi khi thêm dữ liệu vào bảng: {str(e)}"
    except Exception as e:
        # Xử lý các lỗi khác
        message = f"Lỗi không xác định: {str(e)}"

    if not message:
        # Nếu không có lỗi xảy ra
        return templates.TemplateResponse("index.html", {"request": request, "message": message})
    else:
        # Nếu có lỗi, ném một HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=message)

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# khi nhập thì hiện thị luôn
@app.get("/display")
async def addnew(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
