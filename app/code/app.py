from flask import Flask, request, render_template, jsonify
import torch
import torch.nn.functional as F
import pickle
import sys
import os

# Add the main project folder to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)).rsplit('/', 2)[0])

from utils import Skipgram, SkipgramNeg, Glove


app = Flask(__name__)

# Load trained data
skipgram_data = pickle.load(open('app/code/models/skipgrams.pkl', 'rb'))
skipgram_neg_data = pickle.load(open('app/code/models/skipgrams-neg.pkl', 'rb'))
glove_data = pickle.load(open('app/code/models/glove.pkl', 'rb'))

skipgram_word2index = skipgram_data['word2index']
skipgram_neg_word2index = skipgram_neg_data['word2index']
glove_word2index = glove_data['word2index']

skipgram_voc_size = skipgram_data['voc_size']
skipgram_neg_voc_size = skipgram_neg_data['voc_size']
glove_voc_size = glove_data['voc_size']

skipgram_emb_size = skipgram_data['emb_size']
skipgram_neg_emb_size = skipgram_neg_data['emb_size']
glove_emb_size = glove_data['emb_size']

# Instantiate models
skipgram = Skipgram(skipgram_voc_size, skipgram_emb_size, skipgram_word2index)
skipgram.load_state_dict(torch.load('app/code/models/skipgram.pt',
                                    map_location=torch.device('cpu')))
skipgram.eval()

skipgramNeg = SkipgramNeg(skipgram_neg_voc_size, skipgram_neg_emb_size, skipgram_neg_word2index)
skipgramNeg.load_state_dict(torch.load('app/code/models/skipgram-neg.pt',
                                       map_location=torch.device('cpu')))
skipgramNeg.eval()

glove = Glove(glove_voc_size, glove_emb_size, glove_word2index)
glove.load_state_dict(torch.load('app/code/models/glove.pt',
                                 map_location=torch.device('cpu')))
glove.eval()

gensim = pickle.load(open('app/code/models/gensim.pt', 'rb'))


# home page
@app.route('/')
def index():
    return render_template('index.html')


# search page
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        similar_words_results = []  # To store top 10 most similar words for each model

        # Split the query into individual words
        query_words = query.split()

        # Process other models (Skipgram, Skipgram Negative Sampling, GloVe)
        other_models_results = process_models(query_words)
        similar_words_results.append(other_models_results)

        # Process Gensim model
        gensim_results = process_gensim_model(query_words)
        similar_words_results.extend(gensim_results)

        # List model names
        model_names = ["Skipgram", "Skipgram Negative Sampling", "GloVe", "GloVe (Gensim)"]

        return jsonify({
            'query': query,
            'models': model_names,
            'results': similar_words_results
        })


def process_gensim_model(query_words):
    """
    Process the Gensim model to find the top 10 most similar words for the input query.
    """
    combined_vector = None
    for word in query_words:
        # Check if the word exists in the Gensim model
        if word in gensim:
            word_vector = gensim.get_vector(word)
        else:
            word_vector = gensim.get_vector('unknown')

        # Combine vectors using element-wise addition
        if combined_vector is None:
            combined_vector = word_vector
        else:
            combined_vector += word_vector

    # Find the top 10 most similar words using Gensim's most_similar function
    top_similar = gensim.most_similar(combined_vector)
    return [word[0] for word in top_similar[:10]]


def process_models(query_words):
    """
    Process the models (Skipgram, Skipgram Negative Sampling, GloVe)
    to find the top 10 most similar words for the input query.
    """
    similar_words = []  # Store results for all models
    models = [skipgram, skipgramNeg, glove]
    word2index = [skipgram_word2index, skipgram_neg_word2index, glove_word2index]

    for index, model in enumerate(models):
        # Get the vocabulary for the current model
        vocabs = list(word2index[index].keys())

        # Get all word vectors for the current model
        all_word_vectors = torch.stack([model.get_embed(word) for word in vocabs])

        # Combine input query vectors
        combined_vector = None
        for word in query_words:
            if word.lower() in vocabs:
                word_vector = model.get_embed(word.lower())
            else:
                word_vector = model.get_embed('<UNK>')

            # Combine vectors using element-wise addition
            if combined_vector is None:
                combined_vector = word_vector
            else:
                combined_vector += word_vector

        # Calculate cosine similarity between the combined vector and all vocabulary vectors
        similarities = F.cosine_similarity(combined_vector, all_word_vectors)

        # get indices of top 10 most similarities
        top_indices = torch.argsort(similarities, descending=True)[:10]

        # fetch the top words from the vocabulary
        top_words = [vocabs[index.item()] for index in top_indices.view(-1)]
        similar_words.append(top_words[:10])

    return similar_words


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
