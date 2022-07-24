from .models import *
from django.shortcuts import render
from django.contrib import messages
from django.http import *
from .forms import *
import os
import cv2
import numpy as np
from PIL import Image
import pickle
import threading
import time

# Create your views here.


face_clasifier = cv2.CascadeClassifier("data\haarcascade_frontalface_default.xml")
Base_Dir = os.path.dirname(os.path.abspath(__file__))

directory = 'faces'
path = os.path.join(Base_Dir, directory)
if os.path.exists(path) == False:
    os.mkdir(path)


def face_extractor(img):
  grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_clasifier.detectMultiScale(grey, 1.2, 5)

  if faces is ():
    return None

  for (x, y, w, h) in faces:
    croped_faces = img[y:y + h, x:x + w]

  return croped_faces




def home(request):
  return render(request,'examapp/index.html')

def registration(request):
  if request.method=="POST":
    fm=UserForm(request.POST,request.FILES)
    email=request.POST['email']
    password=request.POST['password']
    try:
      usr=User.objects.get(email=email)
      if usr:
        messages.error(request,"This Email Already Exist")
        return render(request,'examapp/registration.html',{'form':fm})
    except:
      if len(password) >= 6 and password.isalnum()==True:
        if fm.is_valid():
          fm.save()
          messages.success(request,"Registration Successfull and Face sample collecttion complete")
          
          fm=UserForm()
          request.session['email']=email
          return HttpResponseRedirect('/dataset/')
      else:
        messages.error(request,"Minimum 6 char or password is not alphanumeric")
        return render(request,'examapp/registration.html',{'form':fm})
      
  else:
    fm=UserForm()

  return render(request,'examapp/registration.html',{'form':fm})

def login(request):
  if request.method=="POST":
    fm=LoginForm(request.POST)
    email=request.POST['email']
    password=request.POST['password']
    try:
      user=User.objects.get(email=email)
      if user:
        if user.password==password:
          request.session['email']=user.email
          request.session['name']=user.firstname+" "+user.lastname
          user.active=True
          user.save()
          usr=User.objects.get(pk=email)
          res=Result.objects.filter(user=user)
          print(res)
          if res:
            return HttpResponseRedirect('/logout/')
          else:
            x="questions/"+user.email
            # print(x)
            return HttpResponseRedirect("/"+x)
        else:
          fm=LoginForm()
          messages.error(request,'Wrong password')
    except:
      messages.error(request,'Invalid Email_id')
  else:
    fm=LoginForm()
  return render(request,'examapp/login.html',{'form':fm})

def logout(request):
  try:
    email=request.session['email']
    user=User.objects.get(pk=email)
    user.active=False
    user.save()
    del request.session['email']
    del request.session['name']
  except:
      pass
  return HttpResponseRedirect('/login/')


def score(request):
  answer=Question.objects.values('correct')
  ids=Question.objects.values('id')
  total=len(answer)
  given=[]
  ans=[]
  ansgiven=[]
  score=0
  for i in range(total):
    try:
      if request.POST['q'+str(i+1)]:
        given.append(request.POST['q'+str(i+1)])
        ansgiven.append(request.POST['q'+str(i+1)])
    except:
      given.append('no_ans')
  
  for k in answer:
    ans.append(k['correct'])
  
  for i in range(total):
    if ans[i] == given[i]:
      score+=1
  
  try:
    email=request.session['email']
    user=User.objects.get(pk=email)
    res=Result(user=user,totalquestion=total,totalgivenans=len(ansgiven),score=score,complete=True)
    res.save()
  except:
      pass
  time.sleep(5)
  return HttpResponseRedirect('/logout/')


def question(request,email):
  ques=Question.objects.all()
  try:
    user=User.objects.get(pk=email)
    if user.active:
      name=request.session['name']
    else:
      return HttpResponseRedirect('/login/')
  except:
    pass
  return render(request,'examapp/question.html',{'name':name,'questions':ques})


def dataset(request):
    Base_Dir = os.path.dirname(os.path.abspath(__file__))
    directory = 'faces'
    path = os.path.join(Base_Dir, directory)
    if os.path.exists(path) == False:
        os.mkdir(path)

    name = request.session['email']
    face_clasifier = cv2.CascadeClassifier(
        "data\haarcascade_frontalface_default.xml")

    def face_extractor(img):
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_clasifier.detectMultiScale(grey, 1.2, 5)

        if faces is ():
            return None

        for (x, y, w, h) in faces:
            croped_faces = img[y:y + h, x:x + w]

        return croped_faces

    cap = cv2.VideoCapture(0)
    count = 0
    start = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if face_extractor(frame) is not None:
            
            face = cv2.resize(face_extractor(frame), (250, 250))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            file_path = os.path.join(path, name)

            if os.path.exists(file_path) == False:
                os.mkdir(file_path)


            if time.time()-start>5:
              count += 1
              file_path = file_path + '/' + str(count) + '.jpg'
              cv2.imwrite(file_path, face)

              cv2.putText(face, str(count), (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 2)
            cv2.imshow("face_croper", frame)

        else:
            pass

        if cv2.waitKey(1) & 0xff == 27 or count == 50:
            break

    cap.release()
    cv2.destroyAllWindows()
    return HttpResponseRedirect("/training/")


def train(request):
    Base_Dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(Base_Dir, 'faces')

    face_clasifier = cv2.CascadeClassifier(
        "data\haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    lable_id = {}
    y_lables = []
    x_trains = []
    for root, dirs, files in os.walk(data_path):
        for file in files:
            path = os.path.join(root, file)
            lable = os.path.basename(root)

            if lable not in lable_id:
                lable_id[lable] = current_id
                current_id += 1

            id_ = lable_id[lable]

            pil_img = Image.open(path).convert('L')
            # print(pil_img)
            img_array = np.array(pil_img, "uint8")
            # print(img_array,end="\n")
            faces = face_clasifier.detectMultiScale(img_array, 1.2, 5)

            for x, y, w, h in faces:
                roi = img_array[y:y + h, x: x + w]
                x_trains.append(roi)
                y_lables.append(id_)

    with open("lable.pickle", "wb") as f:
        pickle.dump(lable_id, f)

    recognizer.train(x_trains, np.array(y_lables))
    recognizer.save("trainner.yml")
    print("Tranning Complete")
    return HttpResponseRedirect("/login/")


face_clasifier = cv2.CascadeClassifier("data\haarcascade_frontalface_default.xml")
def face_detector(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_clasifier.detectMultiScale(grey, 1.2, 5)

    if faces is ():
        return None
    return faces

recognizer = cv2.face.LBPHFaceRecognizer_create()
lable={}

recognizer.read("trainner.yml")
with open("lable.pickle","rb") as f:
    lable=pickle.load(f)
lable={v:k for k,v in lable.items() }

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def face_detector(img):
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_clasifier.detectMultiScale(grey, 1.2, 5)
        
    def get_frame(self):
        image = self.frame
        frame=image

        if face_detector(frame) is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_clasifier.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                roi = gray[y:y + h, x:x + w]
                id_,result=recognizer.predict(roi)
                

                if result < 500:
                    conf=int(100*(1-(result/300)))

                if conf > 80:
                    name=lable[id_]
                    cv2.putText(frame,name,(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

                else:
                    cv2.putText(frame,"Unknown",(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

                
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        else:
          pass
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def livefe(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  
        pass


