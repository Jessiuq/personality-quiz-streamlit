import streamlit as st
import pickle
import re
import os
import numpy as np
import pandas as pd

def initialize_session_state():
    if "step" not in st.session_state:
        st.session_state.step = "info"
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "age" not in st.session_state:
        st.session_state.age = 1  # Initialize with a valid value within the range
    if "birthplace" not in st.session_state:
        st.session_state.birthplace = ""
    if "location" not in st.session_state:
        st.session_state.location = ""
    if "ethnicity" not in st.session_state:
        st.session_state.ethnicity = ""
    if "cumulative_scores" not in st.session_state:
        st.session_state.cumulative_scores = {i: 0 for i in range(1, 10)}
    if "scorecard" not in st.session_state:
        st.session_state.scorecard = {}
    if "perfectionist_scores" not in st.session_state:
        st.session_state.perfectionist_scores = {"intense": 0, "procrastinator": 0, "parisian": 0, "messy": 0, "classic": 0}

def reset_session_state():
    st.session_state.step = "info"
    st.session_state.name = ""
    st.session_state.age = 1  # Initialize with a valid value within the range
    st.session_state.birthplace = ""
    st.session_state.location = ""
    st.session_state.ethnicity = ""
    st.session_state.cumulative_scores = {i: 0 for i in range(1, 10)}
    st.session_state.scorecard = {}
    st.session_state.perfectionist_scores = {"intense": 0, "procrastinator": 0, "parisian": 0, "messy": 0, "classic": 0}
    st.rerun()

def main():
    st.title("Personality Quiz")

    initialize_session_state()

    if st.session_state.step == "info":
        participant_info()
    elif st.session_state.step == "quiz":
        quiz()
    elif st.session_state.step == "results":
        show_results()

def participant_info():
    st.subheader("Participant Information")

    # Name input
    st.session_state.name = st.text_input("Name (first and last)?", value=st.session_state.name)
    if st.session_state.name:
        if not re.match("^[A-Za-z ]+$", st.session_state.name):
            st.error("Name must only contain letters and spaces.")

    # Age input
    st.session_state.age = st.number_input("Age?", min_value=1, max_value=100, step=1, value=st.session_state.age)
    if st.session_state.age:
        if not (1 <= st.session_state.age <= 100):
            st.error("Age must be between 1 and 100.")

    # Birthplace input
    st.session_state.birthplace = st.text_input("Born (e.g., Brooklyn, NY or New York)?", value=st.session_state.birthplace)
    if st.session_state.birthplace:
        if not re.match("^[A-Za-z ]+(, [A-Za-z ]+)*$", st.session_state.birthplace):
            st.error("Birthplace must be formatted as 'City, State', 'State', or 'Country' with no numbers.")

    # Location input
    st.session_state.location = st.text_input("Location (e.g., Queens, NY or New York)?", value=st.session_state.location)
    if st.session_state.location:
        if not re.match("^[A-Za-z ]+(, [A-Za-z ]+)*$", st.session_state.location):
            st.error("Location must be formatted as 'City, State', 'State', or 'Country' with no numbers.")

    # Ethnicity input
    st.session_state.ethnicity = st.text_input("Ethnicity (e.g., German, Chinese)?", value=st.session_state.ethnicity)
    if st.session_state.ethnicity:
        if not re.match("^[A-Za-z ]+(, [A-Za-z ]+)*$", st.session_state.ethnicity):
            st.error("Ethnicity must be formatted as 'Ethnicity1, Ethnicity2' containing only letters and spaces.")

    if st.button("Start Quiz"):
        if not (st.session_state.name and re.match("^[A-Za-z ]+$", st.session_state.name)):
            st.error("Please enter a valid name with only letters and spaces.")
        elif not (1 <= st.session_state.age <= 100):
            st.error("Please enter a valid age between 1 and 100.")
        elif not (st.session_state.birthplace and re.match("^[A-Za-z ]+(, [A-Za-z ]+)*$", st.session_state.birthplace)):
            st.error("Please enter a valid birthplace formatted as 'City, State', 'State', or 'Country' with no numbers.")
        elif not (st.session_state.location and re.match("^[A-Za-z ]+(, [A-Za-z ]+)*$", st.session_state.location)):
            st.error("Please enter a valid location formatted as 'City, State', 'State', or 'Country' with no numbers.")
        elif not (st.session_state.ethnicity and re.match("^[A-Za-z ]+(, [A-Za-z ]+)*$", st.session_state.ethnicity)):
            st.error("Please enter a valid ethnicity containing only letters and spaces.")
        else:
            st.session_state.step = "quiz"
            st.rerun()

def quiz():
    if st.button("Go Back to Demographics"):
        st.session_state.step = "info"
        st.rerun()

    st.subheader("Quiz Instructions")
    st.write("Please answer the following questions. For each question, choose the option that best describes you and enter your confidence interval (1 to 99).")

    questions = [
        {
            "number": 1,
            "question": "When making an important decision that greatly affects your life, which of the following best describes your approach?",
            "options": [
                ("Logical – I carefully consider each option, considering the facts, pros, and cons to make the most logical decision", [5, 6, 7], "classic"),
                ("Emotional – I focus on how each option affects my emotions and aligns with my values to guide my decision", [2, 3, 4], "parisian"),
                ("Instinctual – I rely on my instincts or gut feelings to guide me toward the option that feels intuitively right", [8, 9, 1], "messy")
            ]
        },
        {
            "number": 2,
            "question": "If someone criticizes one of your personality traits that you consider essential to your identity, how are you most likely to feel in the moment?",
            "options": [
                ("Frustrated – I might feel angry towards the person who criticized you or disappointed in how you present yourself to others", [1, 8, 9], "intense"),
                ("Anxious – I might feel uncertain and seek advice on how to improve, or you may need time to reflect and regain confidence", [5, 6, 7], "procrastinator"),
                ("Self-conscious – I might feel ashamed of the trait that was criticized, and consider whether you need to make changes in how you present yourself", [2, 3, 4], "parisian")
            ]
        },
        {
            "number": 3,
            "question": "When you’re in a stressful situation that is out of your control, and you feel nervous about the outcome, what do you usually do to feel better?",
            "options": [
                ("I prefer to spend time alone to focus on managing my feelings and thoughts privately", [5], "procrastinator"),
                ("I reach out to and seek support from others to feel more secure and grounded", [6], "parisian"),
                ("I keep myself occupied with a structured schedule to stay engaged and productive", [7], "messy")
            ]
        },
        {
            "number": 4,
            "question": "When you receive unexpected news, how do you usually react?",
            "options": [
                ("I take time to process it alone, reflecting on its impact and gathering more details", [5], "procrastinator"),
                ("I quickly adapt and focus on finding positives, embracing any opportunities it might bring", [7], "messy"),
                ("I immediately discuss it with someone I trust to gain their perspective and reassurance", [6], "parisian")
            ]
        },
        {
            "number": 5,
            "question": "After failing an important task, how do you typically cope to feel better?",
            "options": [
                ("I reach out to others for reassurance, to feel valued and understood", [2], "parisian"),
                ("I keep trying until I succeed, to demonstrate my capability and feel capable", [3], "intense"),
                ("I focus on my strengths and unique talents, to remind myself of my worth and potential", [4], "messy")
            ]
        },
        {
            "number": 6,
            "question": "When you want to make a good impression on someone, how do you usually approach it?",
            "options": [
                ("I try to make them feel comfortable by offering a small gesture of kindness or consideration", [2], "parisian"),
                ("I highlight my skills or achievements by discussing areas where I feel confident and capable", [3], "intense"),
                ("I share something unique about myself, such as a personal talent or quality that I value", [4], "messy")
            ]
        },
        {
            "number": 7,
            "question": "When an acquaintance wrongs you, how are you most likely to respond?",
            "options": [
                ("I let them know how I feel, openly expressing my anger or frustration", [8], "intense"),
                ("I minimize or ignore my anger to avoid conflict and keep the peace", [9], "parisian"),
                ("I suppress my anger to remain in control of the situation and my emotions", [1], "classic")
            ]
        },
        {
            "number": 8,
            "question": "You’re feeling hesitant about making a big commitment. What might be causing your hesitation?",
            "options": [
                ("I’m thinking about how the commitment will affect me personally and the time or effort it will demand", [8], "messy"),
                ("I am concerned that I might make mistakes and how those could impact the success of the commitment", [1], "procrastinator"),
                ("I am reflecting on how this commitment might affect my emotions and the feelings of those around me", [9], "parisian")
            ]
        },
        {
            "number": 9,
            "question": "In the midst of a stressful situation, how do you typically respond?",
            "options": [
                ("I withdraw and seek solitude, giving myself time to reflect and regain a sense of calm", [4, 5, 9], "procrastinator"),
                ("I focus on finding practical solutions and creating a plan to address the issue directly", [1, 2, 6], "classic"),
                ("I concentrate on my strengths and remind myself of past successes to approach the challenge with confidence", [3, 7, 8], "intense")
            ]
        },
        {
            "number": 10,
            "question": "When something doesn’t go your way, how are you most likely to respond?",
            "options": [
                ("I stay positive and focus on building morale and maintaining an optimistic attitude", [7, 9, 2], "messy"),
                ("I address the issue by analyzing it objectively and look for practical solutions", [3, 1, 5], "classic"),
                ("I process my emotional response to the situation first before I can effectively move forward", [4, 6, 8], "parisian")
            ]
        },
        {
            "number": 11,
            "question": "You receive negative criticism on a project you put a lot of effort into, and it upsets you. How are you likely to respond?",
            "options": [
                ("I take time to process my feelings before deciding how best to proceed", [4, 6], "procrastinator"),
                ("I quickly return to the project, using the criticism to guide my actions and improve", [3, 9], "intense")
            ]
        },
        {
            "number": 12,
            "question": "Think of a goal you’ve set for yourself that turned out to be more challenging and less enjoyable than you expected. How are you most likely to respond?",
            "options": [
                ("I push through the difficulties and continue working towards the goal, determined to see it through", [6, 8], "intense"),
                ("I reevaluate the goal and might try different approaches before deciding if I need to change or abandon it", [4, 7], "messy")
            ]
        },
        {
            "number": 13,
            "question": "You are going through a hard time, and an acquaintance offers to listen. How are you most likely to respond?",
            "options": [
                ("I would likely take them up on their offer, trusting that they genuinely want to help", [2, 9], "parisian"),
                ("I would be cautious, preferring to keep my feelings private since I don’t know them well", [5, 6], "procrastinator")
            ]
        },
        {
            "number": 14,
            "question": "After teaching a new colleague at work everything you know, they get the raise you were hoping for. What is likely to be your immediate reaction?",
            "options": [
                ("I’d feel proud of the role I played in their success, even if I didn’t get the raise", [2, 8], "parisian"),
                ("I’d feel disappointed that I missed out on opportunity I wanted", [1, 3], "classic")
            ]
        },
        {
            "number": 15,
            "question": "Your new neighbor moves in and seems indifferent towards you. How are you more likely to respond?",
            "options": [
                ("I’d make an effort to break the ice and build a friendly relationship", [3, 2], "parisian"),
                ("I’d respect their space and focus on my own life, letting things develop naturally", [1, 5], "classic")
            ]
        },
        {
            "number": 16,
            "question": "In group projects, do you prefer to:",
            "options": [
                ("Take on a role that allows for creative control and shaping the project’s direction", [4, 7], "intense"),
                ("Contribute as a supportive team member, helping others and ensuring the project runs smoothly", [6, 9], "parisian")
            ]
        },
        {
            "number": 17,
            "question": "When deciding whether to go on a work trip with your boss and colleagues, what is more likely to influence your decision?",
            "options": [
                ("I’d consider if the trip will advance my career and align with my personal goals", [3, 1], "classic"),
                ("I’d consider if the trip will be enjoyable, and create a positive experience for me and my colleagues", [2, 7], "messy")
            ]
        },
        {
            "number": 18,
            "question": "As you leave your job for good and reflect on the positive aspects of your time there, what are you more likely to focus on?",
            "options": [
                ("I’d focus on the contributions I made to the company and the impact I had on my coworkers", [1, 8], "classic"),
                ("I’d focus on the personal growth and valuable experiences I gained during my time there", [5, 9], "parisian")
            ]
        },
        {
            "number": 19,
            "question": "When attending a social event, how do you typically feel about your role in the group?",
            "options": [
                ("I prefer engaging actively and making a positive and memorable impact on the group", [7, 8], "messy"),
                ("I prefer to observe and engage selectively, forming meaningful connections with a few people", [4, 5], "parisian")
            ]
        },
        {
            "number": 20,
            "question": "When you’re part of a group project, which role do you tend to prefer?",
            "options": [
                ("I prefer to focus on details and keep everything organized", [1], "classic"),
                ("I prefer to come up with creative ideas and contribute to the brainstorming process", [7], "messy")
            ]
        },
        {
            "number": 21,
            "question": "When faced with a task that you’ve only done a few times before, how do you usually approach it?",
            "options": [
                ("I take responsibility and handle the task on your own, trusting in my abilities to manage it", [1], "classic"),
                ("I seek advice or assistance from others with more experience to ensure the task is completed effectively", [6], "parisian")
            ]
        },
        {
            "number": 22,
            "question": "Your friends decide to eat dinner somewhere, despite them knowing you don’t like the restaurant. How are you more likely to respond?",
            "options": [
                ("I’d propose an alternative restaurant that everyone can enjoy", [1], "messy"),
                ("I’d agree with their choice and go along with their decision, even if it’s not my favorite spot", [9], "procrastinator")
            ]
        },
        {
            "number": 23,
            "question": "When creating a plan for a project you’ve been assigned, how do you prefer to approach it?",
            "options": [
                ("I prefer to create an outline and collaborate with others to gather ideas and feedback before finalizing the plan", [2], "parisian"),
                ("I prefer to make a detailed plan independently first, then seek feedback and make adjustments as needed", [5], "classic")
            ]
        },
        {
            "number": 24,
            "question": "After a busy week, you’ve set aside tomorrow for a day of personal enjoyment and self-care. A new friend calls and asks for your help to move out of their apartment. How are you more likely to respond?",
            "options": [
                ("I’d agree to help with the move, even if it means altering my plans for personal enjoyment", [2], "parisian"),
                ("I’d politely decline, explaining that I need the day for myself to focus on self-care", [7], "messy")
            ]
        },
        {
            "number": 25,
            "question": "You discover that an acquaintance is pursuing the same goal as you. How are you more likely to respond?",
            "options": [
                ("I’d assess and compare my progress with theirs to see where I stand", [3], "intense"),
                ("I’d reach out to them and share ideas, even if it means they might reach the goal first", [2], "parisian")
            ]
        },
        {
            "number": 26,
            "question": "At a social gathering where you don’t know everyone well, how do you usually feel?",
            "options": [
                ("I generally feel comfortable and find it easy to become part of the group", [2], "parisian"),
                ("I often feel alone or disconnected, despite the company", [4], "procrastinator")
            ]
        },
        {
            "number": 27,
            "question": "When tackling a new and unfamiliar task, how do you prefer to approach it?",
            "options": [
                ("I prefer to stick closely to established guidelines or instructions to make sure I’m on the right track", [6], "classic"),
                ("I prefer to introduce my own unique ideas or methods to make the task more tailored to my style", [4], "messy")
            ]
        },
        {
            "number": 28,
            "question": "When you have multiple tasks that need your attention simultaneously, how do you usually manage them?",
            "options": [
                ("I prefer to concentrate on one task at a time to manage everything smoothly", [9], "classic"),
                ("I prefer to move between tasks as it helps me complete everything efficiently", [7], "messy")
            ]
        },
        {
            "number": 29,
            "question": "When your friends come to you for help, what do they usually seek?",
            "options": [
                ("They typically ask for my insight and knowledge on the matter", [5], "classic"),
                ("They often rely on my decisiveness and ability to take charge in situations", [8], "intense")
            ]
        },
        {
            "number": 30,
            "question": "You come across a potentially upsetting news article, what are you more likely to do?",
            "options": [
                ("I would read it to stay informed, even if it might be distressing", [5], "intense"),
                ("I would skip it to protect my mental well-being, avoiding unnecessary stress", [9], "procrastinator")
            ]
        },
        {
            "number": 31,
            "question": "When you’re working on a long-term task, how do you typically approach it?",
            "options": [
                ("I tend to concentrate on the task until it’s finished, sometimes overlooking my other responsibilities", [5], "intense"),
                ("I often have difficulty staying focused, sometimes switching between the task at hand and my other responsibilities", [7], "messy")
            ]
        },
        {
            "number": 32,
            "question": "You have to decide between two job options. How do you prefer to make your decision?",
            "options": [
                ("I prefer to ask others what they would do before making my decision", [6], "parisian"),
                ("I prefer to decide independently without seeking outside opinions", [8], "intense")
            ]
        },
        {
            "number": 33,
            "question": "You start a new hobby and find it more challenging than you anticipated. How are you more likely to respond?",
            "options": [
                ("I’d continue with the hobby, viewing the challenges as opportunities to grow and feel accomplished", [8], "intense"),
                ("I’d explore a different hobby that is more enjoyable and aligns better with my interests", [4], "messy")
            ]
        },
        {
            "number": 34,
            "question": "You start a project with a specific deadline, but halfway through, you realize you don’t have enough time to complete it. What are you more likely to do?",
            "options": [
                ("I’d find shortcuts to ensure completion by the deadline", [3], "intense"),
                ("I’d request an extension to ensure the project is as thorough as intended", [1], "classic")
            ]
        },
        {
            "number": 35,
            "question": "When someone disagrees with you strongly in a discussion, how are you more likely to respond?",
            "options": [
                ("I’d confidently express my perspective and not back down", [8], "intense"),
                ("I’d listen to their point of view, and try to find a way to resolve the conflict", [9], "parisian")
            ]
        },
        {
            "number": 36,
            "question": "You achieve a significant milestone with the support of others. How do you typically feel about this accomplishment?",
            "options": [
                ("I feel a strong sense of gratitude, recognizing the importance of the collaboration and support that made the achievement possible", [6], "parisian"),
                ("I feel proud of what I’ve accomplished, focusing on how it reflects my own capabilities and efforts", [3], "intense")
            ]
        },
        {
            "number": 37,
            "question": "You have been working on a project for a while, and were told that the method in which you do things needs to be changed. How are you likely to respond?",
            "options": [
                ("I’d immediately shift my approach to align with the new requirements, adapting quickly in order to achieve the desired result", [3], "messy"),
                ("I’d prefer to gradually adapt, taking time to understand the new method and integrate it comfortably", [4], "classic")
            ]
        }
    ]

    for q in questions:
        st.subheader(f"Question {q['number']}")
        st.write(q['question'])

        # Retrieve previously selected option if available
        selected_option = st.session_state.get(f"option_{q['number']}", None)
        options = [opt[0] for opt in q['options']]
        if selected_option and selected_option in options:
            index = options.index(selected_option)
            selected_option = st.radio("Options", options, index=index, key=f"option_{q['number']}")
        else:
            selected_option = st.radio("Options", options, key=f"option_{q['number']}")

        confidence_intervals = {}
        for option, _, _ in q['options']:
            key = f"{q['number']}_{option}"
            confidence_value = st.session_state.get(key, 1)
            confidence_intervals[option] = st.number_input(f"Confidence interval for '{option}'", min_value=1, max_value=99, value=confidence_value, step=1, key=key)

        st.session_state.scorecard[q['number']] = {
            "option": selected_option,
            "choice": selected_option,  # Store the selected choice
            "types": next(opt[1] for opt in q['options'] if opt[0] == selected_option),
            "perfectionist_type": next(opt[2] for opt in q['options'] if opt[0] == selected_option),
            "confidence_intervals": confidence_intervals  # Store confidence intervals
        }

    if st.button("Submit All"):
        all_valid = True
        for q in questions:
            selected_option = st.session_state.scorecard[q['number']]['option']
            highest_confidence_option = max(st.session_state.scorecard[q['number']]['confidence_intervals'], key=lambda k: st.session_state.scorecard[q['number']]['confidence_intervals'][k] if st.session_state.scorecard[q['number']]['confidence_intervals'][k] else 0)
            if not st.session_state.scorecard[q['number']]['confidence_intervals'][selected_option] or not (1 <= st.session_state.scorecard[q['number']]['confidence_intervals'][selected_option] <= 99):
                all_valid = False
                st.error(f"Error: Enter a confidence interval between 1 and 99 for the selected option in Question {q['number']}")
                break
            elif selected_option != highest_confidence_option:
                all_valid = False
                st.error(f"Error: You must select the option with the highest confidence interval for Question {q['number']}")
                break

        if all_valid:
            # Update cumulative scores based on confidence intervals
            for q in questions:
                selected_option = st.session_state.scorecard[q['number']]['option']
                for option, types, perfectionist_type in q['options']:
                    confidence_value = st.session_state.scorecard[q['number']]['confidence_intervals'][option]
                    if confidence_value:
                        for enneagram_type in types:
                            st.session_state.cumulative_scores[enneagram_type] += confidence_value
                        st.session_state.perfectionist_scores[perfectionist_type] += confidence_value

            # Save the results and generate the download link
            save_results()
            st.session_state.step = "results"
            st.rerun()

def save_results():
    # Prepare data for JSON-compatible format
    data = {
        "name": st.session_state.name,
        "age": st.session_state.age,
        "birthplace": st.session_state.birthplace,
        "location": st.session_state.location,
        "ethnicity": st.session_state.ethnicity,
        "scorecard": st.session_state.scorecard,
        "cumulative_scores": st.session_state.cumulative_scores,
        "perfectionist_scores": st.session_state.perfectionist_scores  # Add perfectionist scores to data
    }

    # Sanitize and create file name based on the participant's name
    sanitized_name = st.session_state.name.strip().lower().replace(' ', '_')
    file_name = f"{sanitized_name}_responses_and_scores.pkl"

    # Save the data to a pickle file
    with open(file_name, "wb") as f:
        pickle.dump(data, f)

    # Prepare the download button
    with open(file_name, "rb") as f:
        st.download_button(
            label="Download your responses",
            data=f,
            file_name=file_name,
            mime="application/octet-stream"
        )

def show_results():
    st.title("Results")

    st.subheader("Cumulative Scores")
    st.write(st.session_state.cumulative_scores)

    st.subheader("Perfectionist Cumulative Scores")
    st.write(st.session_state.perfectionist_scores)

    dominant_type = max(st.session_state.cumulative_scores, key=st.session_state.cumulative_scores.get)
    st.subheader(f"Dominant Enneagram Type: {dominant_type}")

    dominant_perfectionist = max(st.session_state.perfectionist_scores, key=st.session_state.perfectionist_scores.get)
    st.subheader(f"Dominant Perfectionist Type: {dominant_perfectionist}")

    # Display the download button for the saved results
    save_results()

    if st.button("Restart Quiz"):
        reset_session_state()
        st.rerun()

if __name__ == "__main__":
    main()
