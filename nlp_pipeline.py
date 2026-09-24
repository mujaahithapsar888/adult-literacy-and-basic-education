import spacy
from transformers import pipeline
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
import re

# NLTK setup
try:
    stopwords.words('english')
except:
    nltk.download('stopwords')
    nltk.download('punkt')

# Load Spacy
try:
    nlp = spacy.load("en_core_web_sm")
except:
    # Will be handled if not downloaded yet
    pass

# Load Transformers
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
zero_shot_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def clean_text(text: str) -> str:
    # Basic cleaning
    text = re.sub(r'<[^>]+>', '', text) # HTML tags
    text = re.sub(r'[^a-zA-Z0-9.,!?\'\"\s]', '', text) # Special chars
    return text.strip()

def extract_keywords(texts, top_n=5):
    if isinstance(texts, str):
        texts = [texts]
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        return list(feature_names)
    except:
        return []

def analyze_linguistics(text: str):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    
    return {
        "token_count": len(tokens),
        "lemmatized_words": lemmas[:10], # sample
        "reading_level": textstat.flesch_kincaid_grade(text),
        "reading_ease": textstat.flesch_reading_ease(text),
        "difficult_words": textstat.difficult_words(text)
    }

def analyze_sentiment(text: str):
    # Truncate text for bert token limits
    trunc_text = text[:512]
    res = sentiment_analyzer(trunc_text)[0]
    return {
        "label": res['label'],
        "score": float(res['score'])
    }

def detect_misconceptions(text: str, correct_concepts: list):
    """
    Uses zero shot to see if the text aligns more with misconceptions or correct concepts.
    Here we pass the text and standard labels to see the fit.
    """
    labels = correct_concepts + ["misunderstanding", "factually incorrect", "confusion"]
    res = zero_shot_classifier(text, candidate_labels=labels)
    
    is_misconception = False
    top_label = res['labels'][0]
    if top_label in ["misunderstanding", "factually incorrect", "confusion"]:
        is_misconception = True
        
    return {
        "is_misconception": is_misconception,
        "top_detected_concept": top_label,
        "confidence": float(res['scores'][0])
    }

def generate_grammar_feedback(text: str):
    # A lightweight mockup rule-based feedback system since language-tool requires Java.
    feedback = []
    
    # Check for consecutive spaces or punctuation
    if re.search(r'\s{2,}', text):
        feedback.append("Avoid using multiple consecutive spaces.")
    if re.search(r'[.,!?]{2,}', text):
        feedback.append("Avoid repetitive punctuation (e.g., '!!' or '..').")
        
    # Check capitalization
    sentences = nltk.tokenize.sent_tokenize(text)
    for s in sentences:
        if s and not s[0].isupper():
            feedback.append(f"Sentence should start with a capital letter: '{s[:15]}...'")
            break
            
    if not feedback:
        feedback.append("Grammar and syntax look solid!")
        
    return feedback

def comprehensive_analysis(text: str, expected_concepts: list = None):
    if expected_concepts is None:
        expected_concepts = ["reading comprehension", "logic"]
        
    clean = clean_text(text)
    ling = analyze_linguistics(clean)
    sent = analyze_sentiment(clean)
    misc = detect_misconceptions(clean, expected_concepts)
    keys = extract_keywords(clean)
    grammar = generate_grammar_feedback(clean)
    
    return {
        "cleaned_text_preview": clean[:100] + "...",
        "linguistics": ling,
        "sentiment": sent,
        "misconception_analysis": misc,
        "keywords": keys,
        "grammar_feedback": grammar
    }
