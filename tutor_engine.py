import os
from langchain_huggingface import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
import re

class AITutorEngine:
    def __init__(self, model_id="google/flan-t5-small"):
        # Initialize the HuggingFace Pipeline
        hf_pipeline = pipeline(
            "text2text-generation",
            model=model_id,
            max_length=256,
            temperature=0.7
        )
        self.llm = HuggingFacePipeline(pipeline=hf_pipeline)
        
        # Initialize Session Memory
        self.memory = ConversationBufferMemory()
        
        # Initialize Context Retrieval (RAG)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = self._build_mock_vector_store()
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 2})
        
        # Initialize Safety Filter
        self.banned_words = ["hate", "violence", "cheat", "harm"]
        
        # General Conversation Chain
        template = """You are a helpful and patient AI Tutor for Adult Literacy students.
Previous Conversation:
{history}
Current Context: {context}
Student: {input}
Tutor:"""
        self.prompt = PromptTemplate(input_variables=["history", "input", "context"], template=template)
        
    def _build_mock_vector_store(self):
        # Mock curriculum data
        texts = [
            "Module 1 teaches basic phonics and reading simple sentences.",
            "Module 2 covers intermediate reading comprehension, finding the main idea.",
            "Module 3 focuses on writing short essays and paragraphs.",
            "Time management is crucial for adult learners balancing work and study."
        ]
        return FAISS.from_texts(texts, self.embeddings)
        
    def safety_filter(self, text: str) -> bool:
        # Returns True if safe, False if unsafe
        text_lower = text.lower()
        for word in self.banned_words:
            if re.search(r'\b' + word + r'\b', text_lower):
                return False
        return True

    def chat(self, user_input: str) -> str:
        if not self.safety_filter(user_input):
            return "I'm sorry, but I cannot process that request due to safety policies."
            
        # Retrieve context
        docs = self.retriever.invoke(user_input)
        context = " ".join([d.page_content for d in docs])
        
        # Load history
        history = self.memory.load_memory_variables({})["history"]
        
        # Generate response
        prompt_val = self.prompt.format(history=history, input=user_input, context=context)
        response = self.llm.invoke(prompt_val)
        
        # Save memory
        self.memory.save_context({"input": user_input}, {"output": response})
        return response

    def summarize(self, text: str) -> str:
        prompt = f"Summarize the following chapter in simple terms for an adult learner:\n\n{text}"
        return self.llm.invoke(prompt)

    def generate_hint(self, question: str) -> str:
        prompt = f"Give a helpful, encouraging hint (but not the direct answer) for this question:\n{question}"
        return self.llm.invoke(prompt)

    def generate_flashcards(self, topic: str) -> str:
        prompt = f"Create 3 flashcards (Format: Q: ... A: ...) for the topic: {topic}"
        return self.llm.invoke(prompt)

# Singleton instance
tutor = AITutorEngine()
