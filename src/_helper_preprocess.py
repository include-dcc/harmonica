import pandas as pd
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to process the source_column_value using ChatGPT
def extract_terms(text):
    """Ask ChatGPT if the text contains disease, phenotype, or medical process terms."""
    prompt = (
        f"""
        Identify and categorize any terms in the following text related to diseases, phenotypes, or medical processes. 
        Return a JSON object with keys 'disease', 'phenotype', and 'medical_process' and include the identified terms under each.
        
        Text: {text}
        """
    )

    try:
        # Call ChatGPT API (replace YOUR_API_KEY with your actual OpenAI API key)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response['choices'][0]['message']['content']
        return eval(content)  # Convert JSON-like string to dictionary
    except Exception as e:
        print(f"Error processing text: {text}\nError: {e}")
        return {"disease": [], "phenotype": [], "medical_process": []}

# Load Excel file
def process_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Create an output DataFrame
    results = []

    for _, row in df.iterrows():
        uuid = row['UUID']
        study = row['study']
        source_column = row['source_column']
        source_value = row['source_column_value']

        # Extract terms using ChatGPT
        extracted_terms = extract_terms(source_value)

        print(f"UUID: {uuid} - source_value: {source_value} - extracted_terms: {extracted_terms}\n\n")

        # Add rows for each term found in the relevant category
        for category, terms in extracted_terms.items():
            for term in terms:
                results.append({
                    "UUID": uuid,
                    "study": study,
                    "source_column": source_column,
                    "source_column_value": source_value,
                    "category": category,
                    "term": term,
                })

    # Convert results to a DataFrame
    return pd.DataFrame(results)

# Main function to run the script
def main():
    input_file = "" # Example "../data/input/DS-Determined/extracted_data.xlsx"  # Replace with the path to your input file
    output_file = "output.xlsx"

    # Process the Excel file
    results_df = process_excel(input_file)

    # Save results to a new Excel file
    results_df.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
