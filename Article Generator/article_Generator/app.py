import streamlit as st
import os
import csv
from llm_handler import get_llm_response


# Function to save interaction data
def save_interaction(user_query, llm_name, response):
    file_path = "interactions.csv"
    file_exists = os.path.isfile(file_path)

    # Data to save
    interaction_data = {
        "user_query": user_query,
        "llm_name": llm_name,
        "response": response,
    }

    # Write to the CSV file
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["user_query", "llm_name", "response"])
        if not file_exists:
            writer.writeheader()  # Write header if file is new
        writer.writerow(interaction_data)

# Function to handle article generation
def article_generator():
    st.title("Article Generator with Multiple LLMs")

    # Input from user
    user_query = st.text_area("Enter your article topic or query:")
    selected_llm = st.selectbox("Select an LLM:", ["GPT-Neo 1.3B", "Bloom-560M", "OPT-1.3B"])

    if st.button("Generate Article"):
        if user_query:
            response = get_llm_response(selected_llm, user_query)
            st.write("### Generated Article")
            st.write(response)

            # Save the interaction
            save_interaction(user_query, selected_llm, response)
        else:
            st.warning("Please enter a topic or query.")

# Function to display analytics
def display_analytics():
    st.title("Chatbot Analytics")

    # Check if interactions.csv exists
    file_path = "interactions.csv"
    if os.path.exists(file_path):
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            interactions = list(reader)

        st.write("### Interaction Data")
        st.dataframe(interactions)

        # Display basic analytics
        if interactions:
            total_queries = len(interactions)
            most_used_llm = max(set(row["llm_name"] for row in interactions), key=lambda llm: sum(row["llm_name"] == llm for row in interactions))
            st.write(f"**Total Queries:** {total_queries}")
            st.write(f"**Most Used LLM:** {most_used_llm}")
    else:
        st.warning("No interactions data found.")

# Main function to route pages
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ["Article Generator", "Analytics"])

    if page == "Article Generator":
        article_generator()
    elif page == "Analytics":
        display_analytics()

if __name__ == "__main__":
    main()
