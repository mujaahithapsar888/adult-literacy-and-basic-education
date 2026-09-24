import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_ai_tutor():
    st.title("🧠 AI Tutor")
    st.markdown("Your personal AI assistant to help you understand concepts, practice skills, and navigate your coursework.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI Tutor. How can I help you today?"}
        ]
        
    # Suggested Questions / Quick Buttons
    st.markdown("##### Quick Questions")
    quick_cols = st.columns(4)
    suggested_q = None
    if quick_cols[0].button("Explain Fractions", use_container_width=True):
        suggested_q = "Explain Fractions"
    if quick_cols[1].button("Teach Alphabet", use_container_width=True):
        suggested_q = "Teach Alphabet"
    if quick_cols[2].button("Help with Grammar", use_container_width=True):
        suggested_q = "Help with Grammar"
    if quick_cols[3].button("Solve this Question", use_container_width=True):
        suggested_q = "Solve this Question"
        
    st.markdown("---")
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Voice Input Placeholder (Visual only for now)
    st.markdown(
        """
        <div style="text-align: right; padding-right: 15px; margin-bottom: -15px; position: relative; z-index: 10;">
            <span style="font-size: 20px; cursor: pointer; color: #888;" title="Voice Input (Placeholder)">🎤</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # React to user input
    user_q = st.chat_input("Ask your AI tutor or click the microphone above to speak...")
    
    # Handle both quick buttons and chat input
    prompt = user_q or suggested_q
    
    if prompt:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Simulated typing animation response
            mock_response = f"I'd be happy to help you with **{prompt}**! As an AI tutor, I can explain concepts step-by-step, provide examples, or test your knowledge. What specific part are you struggling with?"
            for chunk in mock_response.split(" "):
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            
            # Final response without cursor
            message_placeholder.markdown(full_response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

def render_writing_evaluation():
    st.title("✍️ Writing Evaluation")
    st.markdown("Practice your writing skills. Enter your text below and get instant AI-powered feedback on grammar, vocabulary, and structure.")
    
    # Input Area
    user_text = st.text_area("Your text:", height=200, placeholder="Start typing your essay or paragraph here...")
    
    if st.button("🔍 Evaluate Text", type="primary"):
        if not user_text.strip():
            st.warning("Please enter some text to evaluate.")
        else:
            with st.spinner("Analyzing your writing..."):
                time.sleep(1.5) # Simulate processing delay
                
            st.success("Evaluation Complete!")
            st.markdown("---")
            
            # Top-level Charts (Gauge and Circle)
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.subheader("Overall Score")
                # Gauge Meter using Plotly Graph Objects
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = 85,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Writing Proficiency"},
                    gauge = {'axis': {'range': [None, 100]},
                             'bar': {'color': "#4361ee"},
                             'steps': [
                                 {'range': [0, 50], 'color': "#ff9999"},
                                 {'range': [50, 75], 'color': "#ffcc99"},
                                 {'range': [75, 100], 'color': "#99ff99"}],
                             'threshold': {
                                 'line': {'color': "red", 'width': 4},
                                 'thickness': 0.75,
                                 'value': 90}}
                ))
                fig_gauge.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
            with chart_col2:
                st.subheader("Progress Circle")
                # Progress Circle (Donut Chart)
                df_progress = pd.DataFrame({'Category': ['Completed', 'Remaining'], 'Value': [85, 15]})
                fig_circle = px.pie(df_progress, values='Value', names='Category', hole=0.7, 
                                    color='Category', color_discrete_map={'Completed': '#4361ee', 'Remaining': '#e0e0e0'})
                fig_circle.update_layout(showlegend=False, height=250, margin=dict(l=10, r=10, t=10, b=10),
                                         annotations=[dict(text='85%', x=0.5, y=0.5, font_size=30, showarrow=False)])
                st.plotly_chart(fig_circle, use_container_width=True)
                
            # Metrics Row
            st.markdown("### Detailed Metrics")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Grammar Score", "88/100", "+2")
            m2.metric("Vocabulary Score", "76/100", "-1")
            m3.metric("Readability", "Grade 8", "Optimal")
            m4.metric("Sentence Structure", "Good", "85%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Feedback Details
            col_feed1, col_feed2 = st.columns(2)
            with col_feed1:
                st.error("🚨 Spelling Errors")
                st.write("- 'teh' -> 'the'")
                st.write("- 'recieve' -> 'receive'")
                st.write("- 'alot' -> 'a lot'")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.warning("💡 Suggestions")
                st.write("- Try using more varied sentence lengths to improve flow.")
                st.write("- Enhance your vocabulary by replacing basic adjectives with stronger ones.")
                
            with col_feed2:
                st.success("✅ Correct Version")
                st.info(f"**Your Text (Corrected):**\n\n{user_text}\n\n*(Note: In a real implementation, this box would display the AI-corrected version of the text you entered above. For now, it mirrors your input.)*")


def render_ai_recommendations():
    st.title("🤖 AI Recommendations")
    st.markdown("Personalized, ML-generated insights to optimize your learning path.")
    
    # Hero Recommendation Card
    st.subheader("🌟 Top Recommendation for You")
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 📘 Course: Advanced Reading Comprehension")
            st.markdown("**Next Best Lesson:** Inferring Context from Complex Sentences")
            st.info("💡 **Why this recommendation?** Your recent Practice Quiz scores showed a 65% accuracy in Reading Comprehension, specifically struggling with context clues. This lesson directly targets that weakness.")
        with col2:
            st.metric("Predicted Success Rate", "88%", "+12%")
            st.metric("Confidence Score", "High (94%)")
            st.button("Start Lesson Now 🚀", type="primary", use_container_width=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Secondary Insights
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📉 Identified Weak Skills")
        with st.container(border=True):
            st.markdown("Our ML models have identified the following areas for improvement based on your historical performance:")
            st.error("- **Contextual Inference** (Current proficiency: 45%)")
            st.warning("- **Vocabulary Variation** (Current proficiency: 60%)")
            st.warning("- **Fraction Subtraction** (Current proficiency: 58%)")
            
    with c2:
        st.subheader("📅 Path Projections")
        with st.container(border=True):
            st.markdown("Based on your current learning velocity (avg. 4.5 hours/week):")
            st.success("**Estimated Course Completion:** October 12, 2026")
            st.info("**Next Assessment Due:** Friday, July 17, 2026")
            st.markdown("*Keep up the current pace to meet these targets!*")

