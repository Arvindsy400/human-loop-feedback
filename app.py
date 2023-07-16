import streamlit as st
import pandas as pd
import base64




# Set up the sidebar with a brief summary of the app
st.sidebar.title("AI Text Extraction Quality Control")
st.sidebar.markdown("This app allows you to assess and improve the quality of text extraction performed by AI models.")


def main():

    st.title("AI Text Extraction Quality Control")
    # Allow the user to upload a CSV file
    st.set_option('deprecation.showfileUploaderEncoding', False)
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        pd.set_option('display.max_colwidth', None)
        st.write(f"**Number of rows extracted by Google Document AI: {len(df)}**", unsafe_allow_html=True)

        # Display each row of the DataFrame and checkboxes
        st.write('Validation Of Doc AI outputs:')
        keep_indices = []
        for i, row in df.iterrows():
            st.write(row[0])
            keep = st.checkbox(f'Mark as correct for row {i+1}')
            if keep:
                keep_indices.append(i)

        # Create the new DataFrame with the selected rows
        new_df = df.iloc[keep_indices]

        # Display the new DataFrame and the rows that were deselected
        st.write('Accurate Extracted Texts:')
        pd.set_option('display.max_colwidth', None)
        st.write(new_df)
        
        deselected_df = df.drop(index=keep_indices)
        st.write('Inaccurate Extracted Texts:')
        pd.set_option('display.max_colwidth', None)
        st.write(deselected_df)
        
        # Calculate accuracy and display it
        accuracy = len(new_df) / len(df)
        st.write(f"Accuracy: {accuracy}")
        
        # Display the survey form
        st.header("Text Extraction Quality Assurance Report")
        name = st.text_input("Name:")
        employee_id = st.text_input("Employee ID:")
        num_missing_words = st.number_input("Number of words that the engine was not able to extract:", min_value=0, step=1)

    # Ask the user for the reason why the engine was not able to extract those words
        reason_missing_words = st.text_area("Plausible reason why the engine was not able to extract those words:")
        relationships = st.selectbox("Rate the AI's ability to understand the relationships between entities, events, or concepts in the extracted text:",
                                    options=["Poor", "Fair", "Good", "Excellent"])
        misunderstandings = st.text_area("Are there any instances where the extracted text misinterpreted or misunderstood the context? Please provide details.")

        st.header("Coherence and Cohesion")
        coherence = st.selectbox("Evaluate the overall coherence and flow of the extracted text:",
                                options=["Incoherent", "Somewhat Coherent", "Mostly Coherent", "Very Coherent"])
        logical_connections = st.checkbox("Does the extracted text demonstrate logical connections between sentences and ideas? Select if yes")
        disjointed = st.text_area("Identify any instances where the extracted text seemed disjointed or lacked logical progression.")

        st.header("Completeness")
        completeness = st.selectbox("Assess the extent to which the extracted text includes all relevant and important information from the source material:",
                                   options=["Incomplete", "Partially Complete", "Mostly Complete", "Fully Complete"])
        missing_details = st.text_area("Identify any significant details or context that were missing from the extracted text.")
        irrelevant_info = st.text_area("Were there any instances where the extracted text included irrelevant or unnecessary information?")

        st.header("Additional Comments")
        additional_comments = st.text_area("Please share any additional comments, observations, or suggestions regarding the quality of the text extracted by the AI.")

        # Optional background information section
        st.header("Optional: Background Information")
        familiar_topic = st.radio("Are you familiar with the topic or domain of the source material?", options=["Yes", "No"])
        expertise_level = st.selectbox("If yes, please rate your expertise level in the topic/domain:",
                                       options=["Novice", "Intermediate", "Expert"])
        specific_concerns = st.text_area("If applicable, please mention any specific concerns or issues related to the topic/domain that you noticed in the extracted text.")

        submit_button = st.button("Submit")

        if submit_button:
            # Generate the text report
            report = f"Text Extraction Quality Survey Report\n\n"
            report += f"Name: {name}\n"
            report += f"Employee ID: {employee_id}\n\n"
            

            report +=f"Missing words"
            report +=f"Number of words that not extracted by Document engines: {num_missing_words}\n"
            report +=f" Plausible reason: {reason_missing_words}\n\n"

            report += "Contextual Understanding\n"
            report += f"The accuracy for the extracted text is found to be: {accuracy*100} %\n"
            report += f"Relationships: {relationships}\n"
            report += f"Misunderstandings: {misunderstandings}\n\n"

            report += "Coherence and Cohesion\n"
            report += f"Coherence: {coherence}\n"
            report += f"Logical Connections: {'Yes' if logical_connections else 'No'}\n"
            report += f"Disjointed: {disjointed}\n\n"

            report += "Completeness\n"
            report += f"Completeness:{completeness}\n"
            report += f"Missing Details: {missing_details}\n"
            report += f"Irrelevant Information: {irrelevant_info}\n\n"

            report += "Additional Comments\n"
            report += f"{additional_comments}\n\n"

            report += "Optional: Background Information\n"
            report += f"Familiar Topic: {familiar_topic}\n"
            report += f"Expertise Level: {expertise_level}\n"
            report += f"Specific Concerns: {specific_concerns}\n"

            # Print the report
            st.text_area("Text Report", value=report, height=400)

             # Download the report as a file
            download_link = generate_download_link(report)
            st.markdown(download_link, unsafe_allow_html=True)

def generate_download_link(report):
    b64 = base64.b64encode(report.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="text_report.txt">Download Text Report</a>'
    return href

if __name__ == '__main__':
    main()
