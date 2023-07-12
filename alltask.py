import streamlit as st
import openai
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

# Set up Azure Form Recognizer client
endpoint = "https://formrcgnr1.cognitiveservices.azure.com/"
key = "5edfb0c6ffd64e9ab79b2649dbeb3bbe"
credential = AzureKeyCredential(key)
form_recognizer_client = FormRecognizerClient(endpoint, credential)

# Set up OpenAI API credentials
openai.api_key = "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"

# Streamlit app code
st.title("Form details providing chatGPT")
st.write("Upload a form and start a chat interaction with ChatGPT")

uploaded_file = st.file_uploader("Upload a form", type=["pdf", "jpg", "png"])

if uploaded_file is not None:
    # Analyze the uploaded form using Azure Form Recognizer
    with st.spinner("Analyzing the form..."):
        result = form_recognizer_client.begin_recognize_content(uploaded_file.read()).result()

    # Extract information from the form
    extracted_text = ""
    for page in result:
        for line in page.lines:
            extracted_text += line.text + " "

    # Start chat interaction
    st.write("Enter your message:")
    user_input = st.text_input("User Input", "")

    if st.button("Send"):
        with st.spinner("Generating response..."):
            # Combine extracted information and user input as prompt
            prompt = f"You provided the following form details: {extracted_text}\nUser: {user_input}"

            # Generate response using ChatGPT
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50,
                temperature=0.7
            ).choices[0].text.strip()

            # Remove question mark from the response
            response = response.replace("?", "")

            # Remove labels from the response
            response = response.replace("Answer:", "")
            response = response.replace("\n", "")

            # Display the response as details in the form
            st.write(response)

            response_dict = {
                "JSON": response.strip()
            }
            st.write(json.dumps(response_dict, indent=4).replace("\\n", "\n"))
