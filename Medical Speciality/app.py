from fastai.text.all import *
import gradio as gr


learn = load_learner('model.pkl')


description = "Medical Diagnosis"
categories = (['Allergy', 'Anemia', 'Bronchitis', 'Diabetes', 'Diarrhea', 'Fatigue', 'Flu', 'Malaria', 'Stress'])



def classify_text(txt):
    pred,idx,probs = learn.predict(txt)
    return dict(zip(categories, map(float,probs)))



text = gr.Textbox(lines=2, label='List out your symptoms to get the possible cause of your symptoms')
label = gr.Label()

# Define custom CSS to adjust the size of the Gradio page
custom_css = """
    .gradio-interface {
        width: 800px; /* Adjust the width as needed */
        height: 600px; /* Adjust the height as needed */
    }
"""


intf = gr.Interface(fn=classify_text, inputs=text, outputs=label, description=description)
intf.launch(inline=False)









