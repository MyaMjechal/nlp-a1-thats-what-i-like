# NLP Assignment 1 (That's What I LIKE)
## Student Information
- **Name:** Mya Mjechal
- **Student ID:** st125469
- **Course:** AIT - Data Science and Artificial Intelligence (DSAI)
- **Assignment:** NLP A1

## About the Project
This project is based on the [`A1_That_s_What_I_LIKE.pdf`](https://github.com/myamjechal/nlp-a1-thats-what-i-like/blob/main/A1_That_s_What_I_LIKE.pdf) document. 

## Dataset
The dataset used in this project is [describe the dataset]. It includes [number] records with [key features].

## Setup Instructions
To set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/myamjechal/nlp-a1-thats-what-i-like.git
    ```
2. Navigate to the project directory:
    ```bash
    cd nlp-a1-thats-what-i-like/app/code
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Download the gensim model and put in app/code/models directory

5. Run the application:
    ```bash
    python app.py
    ```

## Screenshot of Website Working
![Website Screenshot](path/to/screenshot.png)

## Model Comparison and Analysis
| Model          | Window Size | Training Loss | Training Time | Syntatic Accuracy | Semantic Accuracy | Correlation Score (Similarity) |
|----------------|-------------|---------------|---------------|-------------------|-------------------|--------------------------------|
| Skipgram        | 0.85        | 0.80          | 0.82          | 0.81              | 0.81              | 0.81                           |
| Skipgram (NEG)        | 0.88        | 0.85          | 0.86          | 0.85              | 0.85              | 0.85                           |
| GloVe        | 0.90        | 0.87          | 0.88          | 0.88              | 0.88              | 0.88                           |
| GloVe (Gensim)        | 0.90        | 0.87          | 0.88          | 0.88              | 0.88              | 0.88                           |
