from flask import Flask,render_template,request,flash
from werkzeug.utils import secure_filename
import os
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ['png','webp','jpg', 'jpeg']

app = Flask(__name__)
app.secret_key = 'my super secret key'.encode('utf8')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename,operation):
    print(f"the operation is{operation} and filename is{filename}")
    img=cv2.imread(f"uploads/{filename}")

    if operation=="cgray":
        imgprocessed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        newFilename=f"static/{filename}"
        cv2.imwrite(newFilename,imgprocessed)
        return newFilename
    
    elif operation=="cpng":
        newFilename=f"static/{filename.split('.')[0]}.png"
        cv2.imwrite(newFilename,img)
        return newFilename
    
    elif operation=="cwebp":
        newFilename=f"static/{filename.split('.')[0]}.webp"
        cv2.imwrite(newFilename,img)
        return newFilename
    
    elif operation=="cjpg":
        newFilename=f"static/{filename.split('.')[0]}.jpg"
        cv2.imwrite(newFilename,img)
        return newFilename
    
    elif operation=="cjpeg":
        newFilename=f"static/{filename.split('.')[0]}.jpeg"
        cv2.imwrite(newFilename,img)
        return newFilename
    pass
    

@app.route("/")
def home():
    return render_template("/index.html")

@app.route("/edit",methods=['GET','POST'])
def edit():
    if request.method=="POST":
        operation=request.form.get("operation")
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "Error No Selected File"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename,operation)
            flash(f"your image has been processed and is available <a href='/{new}'> here</a>")
            return render_template("/index.html")
    
    return render_template("/index.html")

app.run(debug=True,port=5001)