import cv2
import cv2 as cv
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, Response

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

app = Flask(__name__)
holy_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

index_cord = []  # This list stores values for pointer

def gen_frames():
    global index_cord

    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()

            # To improve performance, optionally mark the image as not writeable
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame)

            # Draw the hand annotations on the image.
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            imgH, imgW = frame.shape[:2]
            string = ''

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Get Hand Coordinates (HC values)
                    hand_cordinate = []
                    for index, landmark in enumerate(hand_landmarks.landmark):
                        x_cordinate, y_cordinate = int(landmark.x * imgW), int(landmark.y * imgH)
                        hand_cordinate.append([index, x_cordinate, y_cordinate])
                    hand_cordinate = np.array(hand_cordinate)

                    # Working on image
                    string = persons_input(hand_cordinate)
                    frame = get_fram(frame, hand_cordinate, string)

            # For pointer
            if string == " D":
                index_cord.append([15, hand_cordinate[8][1], hand_cordinate[8][2]])
            if string == " I" or string == " J":
                index_cord.append([15, hand_cordinate[20][1], hand_cordinate[20][2]])

            for val in index_cord:
                frame = cv.circle(frame, (val[1], val[2]), val[0], (255, 255, 255), 1)
                val[0] = val[0] - 1
                if val[0] <= 0:
                    index_cord.remove(val)

            # Convert the frame to JPEG format and return it to the client
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

def persons_input(hand_cordinates):
    def distance(x1,y1,x2,y2):
        distance=int((((x1-x2)**2)+((y1-y2)**2))**(1/2))
        return distance
    
    persons_input=""
    
    # Consider pawn is Vertical
    hand_horz=False
    
    # Consider all fingure are Down
    thumbs_up=False
    index_up=False
    middel_up=False
    ring_up=False
    littel_up=False
    
    # Here I am using Hand Cordinates(HC) values , which we got from video input.
    # With the help of HC values , I can determine wither the fingure is UP or DOWN
    # In "hand_cordinate[12][1]" , "12" is the index and "1" is X_cordinate (and "2" for Y_cordinate) 
    # For more information, refer the "HAND_CORD" image (to understand the HC)
    
    if distance(hand_cordinates[0][2],0,hand_cordinates[12][2],0) < distance(hand_cordinates[0][1],0,hand_cordinates[12][1],0):
        hand_horz=True
    if distance(hand_cordinates[0][1],hand_cordinates[0][2],hand_cordinates[3][1],hand_cordinates[3][2]) < distance(hand_cordinates[0][1],hand_cordinates[0][2],hand_cordinates[4][1],hand_cordinates[4][2]):
        thumbs_up=True  
    if distance(hand_cordinates[0][1],hand_cordinates[0][2],hand_cordinates[6][1],hand_cordinates[6][2]) < distance(hand_cordinates[0][1],hand_cordinates[0][2],hand_cordinates[8][1],hand_cordinates[8][2]):
        index_up=True
    if distance(hand_cordinates[0][1],hand_cordinates[0][2],hand_cordinates[10][1],hand_cordinates[10][2]) < distance(hand_cordinates[0][1],hand_cordinates[0][2],hand_cordinates[12][1],hand_cordinates[12][2]):
        middel_up=True
    if distance(hand_cordinates[0][1],hand_cordinates[0][2],hand_cordinates[14][1],hand_cordinates[14][2]) < distance(hand_cordinates[0][1],hand_cordinates[0][2],hand_cordinates[16][1],hand_cordinates[16][2]):
        ring_up=True
    if distance(hand_cordinates[0][1],hand_cordinates[0][2],hand_cordinates[18][1],hand_cordinates[18][2]) < distance(hand_cordinates[0][1],hand_cordinates[0][2],hand_cordinates[20][1],hand_cordinates[20][2]):
        littel_up=True
        
    # Get persons_input according to HC values
    
    if index_up==False and middel_up==False and ring_up==False and littel_up==False and thumbs_up==True and hand_horz==False:
        if distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[16][1],hand_cordinates[16][2]) < distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[13][1],hand_cordinates[13][2]):
            persons_input=" O"
        elif distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[18][1],hand_cordinates[18][2]) < distance(hand_cordinates[14][1],hand_cordinates[14][2],hand_cordinates[18][1],hand_cordinates[18][2]):
            persons_input=" M"
        elif distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[18][1],hand_cordinates[18][2]) < distance(hand_cordinates[10][1],hand_cordinates[10][2],hand_cordinates[18][1],hand_cordinates[18][2]):
            persons_input=" N"
        elif distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[18][1],hand_cordinates[18][2]) < distance(hand_cordinates[6][1],hand_cordinates[6][2],hand_cordinates[18][1],hand_cordinates[18][2]):
            persons_input=" T"
        else :
            persons_input=" A"
    elif index_up==True and middel_up==True and ring_up==True and littel_up==True and thumbs_up==True and hand_horz==False:
        if distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[12][1],hand_cordinates[12][2]) < distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[11][1],hand_cordinates[11][2]):
            persons_input=" C"
        elif distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[17][1],hand_cordinates[17][2]) < distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[5][1],hand_cordinates[5][2]):
            persons_input=" B"
    elif index_up==False and middel_up==False and ring_up==False and littel_up==False and thumbs_up==False and hand_horz==False:
        if distance(hand_cordinates[20][1],hand_cordinates[20][2],hand_cordinates[4][1],hand_cordinates[4][2]) < distance(hand_cordinates[19][1],hand_cordinates[19][2],hand_cordinates[4][1],hand_cordinates[4][2]):
            persons_input=" E"
        else:
            persons_input=" S"
    elif index_up==False and middel_up==True and ring_up==True and littel_up==True and thumbs_up==True and hand_horz==False:
        persons_input=" F"
    elif index_up==True and middel_up==False and ring_up==False and littel_up==False and thumbs_up==True and hand_horz==True:
        if distance(hand_cordinates[8][1],hand_cordinates[8][2],hand_cordinates[4][1],hand_cordinates[4][2]) < distance(hand_cordinates[6][1],hand_cordinates[6][2],hand_cordinates[4][1],hand_cordinates[4][2]):
            persons_input=" Q"
        elif distance(hand_cordinates[12][1],hand_cordinates[12][2],hand_cordinates[4][1],hand_cordinates[4][2]) < distance(hand_cordinates[10][1],hand_cordinates[10][2],hand_cordinates[4][1],hand_cordinates[4][2]):
            persons_input=" P"
        else:
            persons_input=" G"
    elif index_up==True and middel_up==True and ring_up==False and littel_up==False and thumbs_up==True and hand_horz==True:
        if distance(hand_cordinates[12][1],hand_cordinates[12][2],hand_cordinates[4][1],hand_cordinates[4][2]) < distance(hand_cordinates[10][1],hand_cordinates[10][2],hand_cordinates[4][1],hand_cordinates[4][2]):
            persons_input=" P"
        else:
            persons_input=" H"
    elif index_up==False and middel_up==False and ring_up==False and littel_up==True and thumbs_up==False and hand_horz==False:
        persons_input=" I"
    elif index_up==False and middel_up==False and ring_up==False and littel_up==True and thumbs_up==False and hand_horz==True:
        persons_input=" J"
    elif index_up==True and middel_up==True and ring_up==False and littel_up==False and thumbs_up==True and hand_horz==False:
        if hand_cordinates[8][1] < hand_cordinates[12][1]:
            persons_input=" R"
        elif distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[14][1],hand_cordinates[14][2]) < distance(hand_cordinates[9][1],hand_cordinates[9][2],hand_cordinates[14][1],hand_cordinates[14][2]):
            if 2*distance(hand_cordinates[5][1],hand_cordinates[5][2],hand_cordinates[9][1],hand_cordinates[9][2]) < distance(hand_cordinates[8][1],hand_cordinates[8][2],hand_cordinates[12][1],hand_cordinates[12][2]):
                persons_input=" V"
            else:
                persons_input=" U"
        elif distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[14][1],hand_cordinates[14][2]) < distance(hand_cordinates[5][1],hand_cordinates[5][2],hand_cordinates[14][1],hand_cordinates[14][2]):
            persons_input=" K"
    elif index_up==True and middel_up==False and ring_up==False and littel_up==False and thumbs_up==True and hand_horz==False:
        if distance(hand_cordinates[3][1],hand_cordinates[3][2],hand_cordinates[14][1],hand_cordinates[14][2]) < distance(hand_cordinates[14][1],hand_cordinates[14][2],hand_cordinates[4][1],hand_cordinates[4][2]):
            persons_input=" L"
        elif distance(hand_cordinates[8][1],hand_cordinates[8][2],hand_cordinates[10][1],hand_cordinates[10][2]) < distance(hand_cordinates[6][1],hand_cordinates[6][2],hand_cordinates[10][1],hand_cordinates[10][2]):
            persons_input=" X"
        else:
            persons_input=" D"
    elif index_up==True and middel_up==True and ring_up==False and littel_up==False and thumbs_up==False and hand_horz==False:
        if hand_cordinates[8][1] < hand_cordinates[12][1]:
            persons_input=" R"
        elif 2*distance(hand_cordinates[5][1],hand_cordinates[5][2],hand_cordinates[9][1],hand_cordinates[9][2]) < distance(hand_cordinates[8][1],hand_cordinates[8][2],hand_cordinates[12][1],hand_cordinates[12][2]):
            persons_input=" V"
        else:
            persons_input=" U"
    elif index_up==True and middel_up==True and ring_up==True and littel_up==False and thumbs_up==True and hand_horz==False:
        persons_input=" W"
    elif index_up==False and middel_up==False and ring_up==False and littel_up==True and thumbs_up==True and hand_horz==False:
        if distance(hand_cordinates[3][1],hand_cordinates[3][2],hand_cordinates[18][1],hand_cordinates[18][2]) < distance(hand_cordinates[4][1],hand_cordinates[4][2],hand_cordinates[18][1],hand_cordinates[18][2]):
            persons_input=" Y"
        else:
            persons_input=" I"
        
    return persons_input

#____________________________________________________________geting_in_frame________________________________________________________
def get_fram(image,hand_cordinate,string):
   def x_max(hand_cordinate):
      max_val=0
      for cordinate_list in hand_cordinate:
         if max_val<cordinate_list[1]:    # 1 is x-cord value
            max_val=cordinate_list[1]
      return max_val
   def y_max(hand_cordinate):
      max_val=0
      for cordinate_list in hand_cordinate:
         if max_val<cordinate_list[2]:    # 2 is y-cord value
            max_val=cordinate_list[2]
      return max_val
   def x_min(hand_cordinate):
      min_val=hand_cordinate[0][1]
      for cordinate_list in hand_cordinate:
         if min_val>cordinate_list[1]:
            min_val=cordinate_list[1]
      return min_val
   def y_min(hand_cordinate):
      min_val=hand_cordinate[0][2]
      for cordinate_list in hand_cordinate:
         if min_val>cordinate_list[2]:
            min_val=cordinate_list[2]
      return min_val
   
    
   def show_holy_rect(image,start_point,end_point,string):
    maxX=image.shape[1]
    # To create farme which contain hand
    image = cv.rectangle(image, start_point, end_point, (0,0,255), 1)
    # To create frame for letter 
    image = cv.rectangle(image,(start_point[0],start_point[1]+23),(end_point[0],start_point[1]+3),(0,0,255),-1)
    
    # Write letter in the frame
    image = cv.putText(image, string, (start_point[0]-7,start_point[1]+20), cv.FONT_HERSHEY_SIMPLEX, 1, (300,300,300), 1, cv.LINE_AA)
    return image

   image=show_holy_rect(image,(x_min(hand_cordinate)-7,y_max(hand_cordinate)+7),(x_max(hand_cordinate)+7,y_min(hand_cordinate)-7),string)

   return image
# Create a route in Flask that will display the hand gesture recognition when clicked
@app.route('/')
def index():
    return render_template('index.html')

# Create a route in Flask that will start the hand gesture recognition when clicked
@app.route('/start')
def start():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port='5001')