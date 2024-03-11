from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from eye_tracker import Eye_tracker
from video import Video
from heatmap import Heatmap
from threading import Thread
from PIL import Image
from l2cs import Pipeline, select_device
import re
import pathlib


CWD = pathlib.Path.cwd()
app = FastAPI()

tracker = Eye_tracker()
thread_boucle = Thread(target=tracker.boucle)


image = ''

coord_image = []

s_width = 0
s_height = 0

screen = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    fichier = open('html/window-size.html', 'r')
    contenu = fichier.read()
    fichier.close()
    return contenu


@app.get("/choix-oeuvre", response_class=HTMLResponse)
async def formulaire_choix(request: Request):
    fichier = open('html/formulaire_choix.html', 'r')
    contenu = fichier.read()
    fichier.close()
    return contenu

@app.get("/window-size")
async def get_window_size(request: Request, width: int, height: int):
    global s_height,s_width
    print(f"Width: {width}, Height: {height}")
    s_width = width
    s_height = height
    return {"message": "Window size received successfully"}

@app.get("/callibrage", response_class=HTMLResponse)
async def callibrage(request: Request):

    try :
        tracker.initialisation(s_width,s_height)
    except Exception as e :
        print(e)
    try :
        
        tracker.results_calibration_coord = []
        tracker.calibration_points = []
        fichier = open('html/callibrage.html', 'r')
        contenu = fichier.read()
        fichier.close()
    except Exception as e :
        print(e)
    return contenu

@app.get("/callibre")
async def add_point(i: int):
    rep = tracker.add_callibration(i)
    return "OK"

@app.post("/regard", response_class=HTMLResponse)
async def regard(request: Request): #On initialise la page du regard, on initialise la matrice  et on start la boucle while du regard
    global image, thread_boucle
    tracker.run = True
    try :
        
        data_str = await request.body()
        data = data_str.decode()
        data = data.split("=")
        image = data[1]

    except Exception as e:
        print(e)

    try :
        thread_boucle.start()
    except Exception as e :
        print(e)

    fichier = open('html/regard.html', 'r')
    contenu = fichier.read()
    fichier.close()
    return contenu
    
@app.get("/where-is-gaze")
async def where_is_gaze():
    
    x, y = tracker.transform_eye_calib[0],tracker.transform_eye_calib[1]
    print(x, y)
    res = str(x)+ ' ' + str(y)
    return HTMLResponse(content = str(res))


@app.get("/add-image", response_class=FileResponse)
async def add_image():
    global image
    try: 
        return FileResponse(f"oeuvres/{image}.jpg", media_type="image/jpeg")
    except Exception as e :
        print(e) 
    
@app.get("/add-sound", response_class=FileResponse)
async def add_image():
    global image
    try:
        return FileResponse(f"oeuvres/{image}.mp3", media_type="audio/mpeg")
    except Exception as e :
        print(e) 
        
        
@app.get("/stop")
async def stop():
    global thread_boucle
    tracker.cam.release()
    tracker.run = False
    thread_boucle.join()

@app.get("/analyse", response_class=HTMLResponse)
async def analyse(x1, y1, x2, y2, width, height):
    global coord_image, screen
    screen = [float(width), float(height)]
    coord_image = [[float(x1), float(y1)],[float(x2), float(y2)]]
    print(x1, y1, x2, y2)
    fichier = open('html/analyse.html', 'r')
    contenu = fichier.read()
    fichier.close()
    return contenu
    
    

@app.get("/add-video", response_class=FileResponse)
async def add_video():
    global image, coord_image, screen
    print("add-heatmap")
    try:
        video = Video("coor.txt", "oeuvres/LA_VIERGE_A_L_ENFANT_ENTRE_SAINT_GEORGES_ET_SAINT_JACQUES.jpg", screen, coord_image)
        video_path = video.make_video()
        print("video "+ video_path)
        return FileResponse(video_path, media_type="video/mp4")
    except Exception as e:
        print(e)
        
@app.get("/add-heatmap", response_class=FileResponse)
async def add_heatmap():
    global coord_image
    print("add-heatmap")
    
    try:
        heatmap = Heatmap().make_heatmap2(coord_image, screen)
        print("heatmap "+ heatmap)
        return FileResponse(heatmap, media_type="image/png")
    except Exception as e:
        print(e)
