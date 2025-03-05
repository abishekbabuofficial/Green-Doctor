from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from PIL import Image
from ultralytics import YOLO


def load_model():
    model = YOLO('best.pt')
    return model

# Set up API key
GROQ_API = "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"
client = Groq(api_key=GROQ_API)

def chatbot_response(user_input):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant who assists with gardening queries accurately."},
            {"role": "user", "content": user_input}
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

# Load the model
model = load_model()

# Initialize the Flask app
app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/*": {"origins": ["http://localhost", "http://localhost:5173"]}})

def classify_plant_disease(image, model):
    results = model(image)
    probs = results[0].probs  # Get the probability object
    predicted_class_index = probs.top1  # Get index of the highest probability class
    predicted_class_name = results[0].names[predicted_class_index]
    labels = predicted_class_name
    confs = probs.top1conf.item()
    return labels, confs

@app.route("/predict/<plant>", methods=["POST"])
def predict(plant):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    img = Image.open(file.stream)
    print(type(img))
    # img = np.expand_dims(img, 0)
    
    # Perform prediction
    label, conf = classify_plant_disease(img, model)

    print("Predicted!!\n\nLabel:", label, "\nConfidence:", conf)

    prompt = f"What are the prevention, cure, and symptoms for the {label} disease in plants with two points in each?"
    detailed_response = chatbot_response(prompt)
    
    return jsonify({
        'class': label,
        'confidence': float(conf),
        'details': detailed_response
    })

if __name__ == "__main__":
    app.run(host='localhost', port=8000, debug=True)




# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn
# import numpy as np
# from io import BytesIO
# from PIL import Image
# import tensorflow as tf
# from keras.models import load_model
# from keras.preprocessing import image
# model = load_model("potatoes.h5")

# app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:5173", #5174 is the port where frontend is running
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # model = tf.keras.models.load_model("../saved_models/AlexNetModel.hdf5")
# # tomato_MODEL = tf.keras.models.load_model("../saved_models/tomato_model")
# # pepper_MODEL = tf.keras.models.load_model("../saved_models/pepper_model")
# # groundnut_MODEL = tf.keras.models.load_model("../saved_models/groundnut_model")
# # blackgram_MODEL = tf.keras.models.load_model("../saved_models/blackgram_model")
# cl = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']
# # cl = ['Early Blight', 'Late Blight', 'YellowLeaf Curl Virus', 'Mosaic Virus', 'Healthy']
# # t_CLASS_NAMES = ['Early Blight', 'Late Blight', 'YellowLeaf Curl Virus', 'Mosaic Virus', 'Healthy']
# # pep_CLASS_NAMES = ['Bell Bacterial Spot', 'Bell Healthy']
# # g_CLASS_NAMES = ['Early Leaf Spot', 'Early Rust', 'Healthy Leaf', 'Late Leaf Spot', 'Nutrition Deficiency', 'Rust']
# # b_CLASS_NAMES = ['Anthracnose', 'Healthy', 'Leaf Crinckle', 'Powdery Mildew', 'Yellow Mosaic']

# def read_file_as_image(data) -> np.ndarray:
#     img = Image.open(BytesIO(data)).convert("RGB")
#     target_size = (256, 256)
#     img = img.resize(target_size)
#     # return np.array(img)
#     return image.img_to_array(img)

# @app.post("/predict/{plant}")
# async def predict(plant,file: UploadFile = File(...)):
#     img = read_file_as_image(await file.read())
#     print(img)
#     img = np.expand_dims(img, 0)
#     # img = img/255

#     # img_batch = image.load_img(image, target_size=(224, 224))
#     # img = image.img_to_array(img_batch)
#     # img = np.expand_dims(img, axis=0)
#     # img = img/255
    
#     # if plant == "potato":
#     #     predictions = potato_MODEL.predict(img_batch)
#     #     predicted_class = cl[np.argmax(predictions[0])]
#     # elif plant == "tomato":
#     #     predictions = tomato_MODEL.predict(img_batch)
#     #     predicted_class = t_CLASS_NAMES[np.argmax(predictions[0])]
#     # elif plant == "pepper":
#     #     predictions = pepper_MODEL.predict(img_batch)
#     #     predicted_class = pep_CLASS_NAMES[np.argmax(predictions[0])]
#     # elif plant == "groundnut":
#     #     predictions = groundnut_MODEL.predict(img_batch)
#     #     predicted_class = g_CLASS_NAMES[np.argmax(predictions[0])]
#     # else :
#     prediction = model.predict(img)
#     predicted_class = cl[np.argmax(prediction[0])]
#     # d = prediction.flatten()
#     # j = d.max()
#     # for index,item in enumerate(d):
#     #     if item == j:
#     #         predicted_class = cl[index]
#     confidence = np.max(prediction[0])
#     return {
#         'class': predicted_class,
#         'confidence': float(confidence)
#     }

# ''' 
# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     image = read_file_as_image(await file.read())
#     img_batch = np.expand_dims(image, 0)
    
#     predictions = potato_MODEL.predict(img_batch)

#     predicted_class = p_CLASS_NAMES[np.argmax(predictions[0])]
#     confidence = np.max(predictions[0])
#     return {
#         'class': predicted_class,
#         'confidence': float(confidence)
#     }'''

# if __name__ == "__main__":
#     uvicorn.run(app, host='localhost', port=8000)