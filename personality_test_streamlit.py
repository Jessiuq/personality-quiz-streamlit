import streamlit as st
import pickle
import re


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
    if "cumulative_scores" not in st.session_state:
        st.session_state.cumulative_scores = {i: 0 for i in range(1, 10)}
    if "scorecard" not in st.session_state:
        st.session_state.scorecard = {}


def reset_session_state():
    st.session_state.step = "info"
    st.session_state.name = ""
    st.session_state.age = 1  # Initialize with a valid value within the range
    st.session_state.birthplace = ""
    st.session_state.location = ""
    st.session_state.cumulative_scores = {i: 0 for i in range(1, 10)}
    st.session_state.scorecard = {}
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
    st.session_state.birthplace = st.text_input("Born (e.g., Brooklyn, NY)?", value=st.session_state.birthplace)
    if st.session_state.birthplace:
        if not re.match("^[A-Za-z ]+, [A-Za-z ]+$", st.session_state.birthplace):
            st.error("Birthplace must be formatted as 'City, State' with no numbers.")

    # Location input
    st.session_state.location = st.text_input("Location (e.g., Queens, NY)?", value=st.session_state.location)
    if st.session_state.location:
        if not re.match("^[A-Za-z ]+, [A-Za-z ]+$", st.session_state.location):
            st.error("Location must be formatted as 'City, State' with no numbers.")

    if st.button("Start Quiz"):
        if not (st.session_state.name and re.match("^[A-Za-z ]+$", st.session_state.name)):
            st.error("Please enter a valid name with only letters and spaces.")
        elif not (1 <= st.session_state.age <= 100):
            st.error("Please enter a valid age between 1 and 100.")
        elif not (st.session_state.birthplace and re.match("^[A-Za-z ]+, [A-Za-z ]+$", st.session_state.birthplace)):
            st.error("Please enter a valid birthplace formatted as 'City, State' with no numbers.")
        elif not (st.session_state.location and re.match("^[A-Za-z ]+, [A-Za-z ]+$", st.session_state.location)):
            st.error("Please enter a valid location formatted as 'City, State' with no numbers.")
        else:
            st.session_state.step = "quiz"
            st.rerun()


def quiz():
    st.title("Personality Quiz")

    if st.button("Go Back to Demographics"):
        st.session_state.step = "info"
        st.rerun()

    st.subheader("Quiz Instructions")
    st.write(
        "Please answer the following questions. For each question, choose the option that best describes you and enter your confidence interval (0.1 to 9.9).")

    questions = [
        {
            "number": 1,
            "question": "When making a significant decision (such as choosing a career path), which aspect do you primarily rely on?",
            "options": [
                ("My reasoning – I carefully consider each option and choose the one that makes the most logical sense",
                 [5, 6, 7]),
                (
                "My feelings – I pay attention to how each option affects my emotions and let these feelings guide my decision",
                [2, 3, 4]),
                ("My intuition – I trust my instincts about which option feels right and follow that gut feeling",
                 [8, 9, 1])
            ]
        },
        {
            "number": 2,
            "question": "You find out someone has criticized one of your personality traits that you feel is essential to who you are. How are you most likely to immediately feel?",
            "options": [
                (
                "Angry – either at the person who criticized you or at yourself for how you present yourself to others",
                [1, 8, 9]),
                (
                "Afraid – feeling insecure and wanting guidance on how to improve, or needing time to reassess and reassure yourself",
                [5, 6, 7]),
                (
                "Ashamed – of the trait that was criticized, feeling that you might need to change to present yourself better",
                [2, 3, 4])
            ]
        },
        {
        #     "number": 3,
        #     "question": "When in a stressful situation that is out of your control, and you are nervous about the outcome, what do you do to feel better?",
        #     "options": [
        #         ("Isolate yourself from others", [5]),
        #         ("Seek out security from others", [6]),
        #         ("Keep yourself busy with a structured schedule", [7])
        #     ]
        # },
        # {
        #     "number": 4,
        #     "question": "When you think of a place where you feel the safest, what first comes to mind?",
        #     "options": [
        #         ("Somewhere quiet, where I can be alone and have time to reflect", [5]),
        #         ("A place full of activity and people, where there is always something to keep me occupied", [7]),
        #         (
        #         "A place where I can choose to be around people and distractions but can retreat to a quieter spot if needed",
        #         [6])
        #     ]
        # },
        # {
        #     "number": 5,
        #     "question": "You fail an important task. To feel better, do you:",
        #     "options": [
        #         ("Seek reassurance from others", [2]),
        #         ("Keep trying until you succeed", [3]),
        #         ("Focus on your strengths and unique talents instead of the failure", [4])
        #     ]
        # },
        # {
        #     "number": 6,
        #     "question": "You are told to make a good impression on someone. What are you most likely to do?",
        #     "options": [
        #         ("Do something nice to make them feel comfortable, like buying them a coffee", [2]),
        #         ("Speak about an area you feel confident in, such as your career goals or achievements", [3]),
        #         ("Share something you appreciate about yourself, like your artistic talents", [4])
        #     ]
        # },
        # {
        #     "number": 7,
        #     "question": "An acquaintance has wronged you. Are you more likely to:",
        #     "options": [
        #         ("Let them know and/or express your anger", [8]),
        #         ("Deny your anger to keep the peace", [9]),
        #         ("Repress your anger to stay in control", [1])
        #     ]
        # },
        # {
        #     "number": 8,
        #     "question": "You’re about to make a big commitment but are feeling hesitant. What is most likely the reason?",
        #     "options": [
        #         (
        #         "You are thinking about how the commitment will affect you personally and the level of investment it requires",
        #         [8]),
        #         (
        #         "You are considering the possibility of making mistakes and how they might impact the commitment", [1]),
        #         ("You are reflecting on the potential emotional consequences and the effects on yourself and others",
        #          [9])
        #     ]
        # },
        # {
        #     "number": 9,
        #     "question": "In the midst of a stressful situation, how do you typically respond?",
        #     "options": [
        #         ("Withdraw and seek solitude to reflect and regain a sense of calm", [4, 5, 9]),
        #         ("Focus on identifying practical solutions and steps to address and resolve the issue", [1, 2, 6]),
        #         (
        #         "Concentrate on your strengths and positive attributes to build your confidence and tackle the challenge",
        #         [3, 7, 8])
        #     ]
        # },
        # {
        #     "number": 10,
        #     "question": "Something doesn’t go your way. What is your more likely response?",
        #     "options": [
        #         ("Stay positive and build morale", [7, 9, 2]),
        #         ("Try to solve the problem objectively and logically", [3, 1, 5]),
        #         ("Have an emotional response that needs to be dealt with first", [4, 6, 8])
        #     ]
        # },
        # {
        #     "number": 11,
        #     "question": "You receive negative criticism on a project you worked hard on, which makes you upset. Are you more likely to:",
        #     "options": [
        #         ("Take time to reflect on your feelings before continuing the project", [4, 6]),
        #         ("Quickly return to the project to make improvements and move forward", [3, 9])
        #     ]
        # },
        # {
        #     "number": 12,
        #     "question": "Think of a goal you’ve set for yourself but found it more difficult and less enjoyable than you originally thought. Are you more likely to:",
        #     "options": [
        #         ("Continue working towards the goal despite the challenges", [6, 8]),
        #         ("Reconsider and try a couple of times before potentially changing the goal", [4, 7])
        #     ]
        # },
        # {
        #     "number": 13,
        #     "question": "You are going through a hard time, and an acquaintance notices and asks if you want to talk about it. Are you more likely to:",
        #     "options": [
        #         ("Take them up on their offer and trust that they want to help you", [2, 9]),
        #         ("Be cautious since you don’t know them well and keep your emotions to yourself", [5, 6])
        #     ]
        # },
        # {
        #     "number": 14,
        #     "question": "At work, you teach your new colleague everything you know. They then get the raise that you wanted. What is likely to be your immediate reaction?",
        #     "options": [
        #         ("Feel proud for the role you played in their success", [2, 8]),
        #         ("Feel disappointed for missing the opportunity", [1, 3])
        #     ]
        # },
        # {
        #     "number": 15,
        #     "question": "Your new neighbor moves in and immediately shows their indifference towards you. Are you more likely to:",
        #     "options": [
        #         ("Make an effort to introduce yourself and build a friendly relationship", [3, 2]),
        #         ("Respect their space and let things develop naturally", [1, 5])
        #     ]
        # },
        # {
        #     "number": 16,
        #     "question": "For projects, do you prefer to:",
        #     "options": [
        #         ("Take on a role that allows for creative control and direction", [4, 7]),
        #         ("Contribute as a supportive team member", [6, 9])
        #     ]
        # },
        # {
        #     "number": 17,
        #     "question": "You are deciding whether to go on a work trip with your boss and colleagues. What is more likely to help you make the decision?",
        #     "options": [
        #         ("Considering if the trip will benefit your career and personal goals", [3, 1]),
        #         ("Considering if the trip will be enjoyable for you and your colleagues", [2, 7])
        #     ]
        # },
        # {
        #     "number": 18,
        #     "question": "You are leaving a job for good, and reflecting on the positive outcomes of your work experience. Are you more likely to focus on:",
        #     "options": [
        #         ("The contributions you made to the company and your coworkers", [1, 8]),
        #         ("The personal growth and experiences you gained from the job", [5, 9])
        #     ]
        # },
        # {
        #     "number": 19,
        #     "question": "When you walk into a room, are you more likely to:",
        #     "options": [
        #         ("Expect people to notice and react to your presence", [7, 8]),
        #         ("Assume people will not pay much attention to you", [4, 5])
        #     ]
        # },
        # {
        #     "number": 20,
        #     "question": "When working on a group project, do you prefer to:",
        #     "options": [
        #         ("Work on details and organization", [1]),
        #         ("Brainstorm ideas", [7])
        #     ]
        # },
        # {
        #     "number": 21,
        #     "question": "When you need to complete a task that you have done only a few times before, do you tend to:",
        #     "options": [
        #         ("Trust your own abilities and handle the task yourself", [1]),
        #         ("Rely on others' expertise/abilities and ask for help", [6])
        #     ]
        # },
        # {
        #     "number": 22,
        #     "question": "Your friends decide to eat dinner somewhere, despite them knowing you don’t like the restaurant. Are you more likely to:",
        #     "options": [
        #         ("Suggest finding a different restaurant that everyone can enjoy", [1]),
        #         ("Go along with what your friends decided", [9])
        #     ]
        # },
        # {
        #     "number": 23,
        #     "question": "At a party, do you usually feel more comfortable:",
        #     "options": [
        #         ("Interacting with other people", [2]),
        #         ("Staying by yourself or with who you came with", [5])
        #     ]
        # },
        # {
        #     "number": 24,
        #     "question": "You have had a busy week and have set aside tomorrow as a day to relax and unwind. A friend calls and asks for your help to move out of their apartment. How do you respond?",
        #     "options": [
        #         ("Agree to help your friend, even though it means changing your plans for the day", [2]),
        #         ("Politely explain that you need to use the day to relax and recharge", [7])
        #     ]
        # },
        # {
        #     "number": 25,
        #     "question": "You find out your acquaintance is attempting to reach the same goal as you, what are you more likely to do:",
        #     "options": [
        #         ("Compare your progress with their progress", [3]),
        #         ("Reach out to them and share ideas, even if it means they might reach the goal first", [2])
        #     ]
        # },
        # {
        #     "number": 26,
        #     "question": "When in a social gathering where you don’t know everyone well, do you usually:",
        #     "options": [
        #         ("Feel comfortable and part of the group", [2]),
        #         ("Feel alone despite the company", [4])
        #     ]
        # },
        # {
        #     "number": 27,
        #     "question": "When following a cooking recipe of something unlike anything you’ve made before, are you more likely to:",
        #     "options": [
        #         ("Follow the recipe exactly", [6]),
        #         ("Add your own special touch to it", [4])
        #     ]
        # },
        # {
        #     "number": 28,
        #     "question": "When you have several tasks that need your attention at the same time, how are you more likely to handle the situation?",
        #     "options": [
        #         ("I stay calm and focus on one task at a time to manage everything smoothly", [9]),
        #         ("I enjoy moving between tasks as it helps me complete everything efficiently", [7])
        #     ]
        # },
        # {
        #     "number": 29,
        #     "question": "When your friends ask you for help, it is usually:",
        #     "options": [
        #         ("For your insight and knowledge", [5]),
        #         ("For your strength and decisiveness", [8])
        #     ]
        # },
        # {
        #     "number": 30,
        #     "question": "You see a potentially upsetting news article, are you more likely to:",
        #     "options": [
        #         ("Read it to stay informed, even if it might be distressing", [5]),
        #         ("Avoid it to maintain your peace of mind", [9])
        #     ]
        # },
        # {
        #     "number": 31,
        #     "question": "When working on a task that takes a long time, do you usually:",
        #     "options": [
        #         ("Concentrate on it until it's done, sometimes overlooking other responsibilities", [5]),
        #         ("Have difficulty focusing on it, often turning to other responsibilities", [7])
        #     ]
        # },
        # {
        #     "number": 32,
        #     "question": "You have to decide between two job options. Do you prefer to:",
        #     "options": [
        #         ("Seek advice from others before making your decision", [6]),
        #         ("Decide independently without seeking outside opinions", [8])
        #     ]
        # },
        # {
        #     "number": 33,
        #     "question": "You start a new hobby that is turning out to involve a lot more struggles than you previously thought. Are you more likely to:",
        #     "options": [
        #         ("Persist with the hobby, believing that overcoming the challenges will make it more rewarding", [8]),
        #         ("Switch to another hobby that feels more enjoyable and less challenging", [4])
        #     ]
        # },
        # {
        #     "number": 34,
        #     "question": "You start a project with a specific deadline, and halfway though realize you don’t have enough time to complete it. What are you more likely to do?:",
        #     "options": [
        #         ("Find shortcuts to ensure completion by the deadline", [3]),
        #         ("Request an extension to ensure the project is as thorough as intended", [1])
        #     ]
        # },
        # {
        #     "number": 35,
        #     "question": "A neighbor you haven’t known for too long insults you for the first time. Are you more likely to:",
        #     "options": [
        #         ("Become angry and express this anger towards your neighbor", [8]),
        #         ("Remain calm initially, but become angry if the behavior continues", [9])
        #     ]
        # },
        # {
        #     "number": 36,
        #     "question": "You achieve a significant milestone with the support of others. How do you generally feel about this accomplishment?",
        #     "options": [
        #         (
        #         "Pleased and appreciative, valuing the collaborative effort and the support received in reaching the goal.",
        #         [6]),
        #         (
        #         "Proud of the achievement, focusing on how it reflects your own capabilities and the success you’ve demonstrated.",
        #         [3])
        #     ]
        # },
        # {
        #     "number": 37,
        #     "question": "You have been working on a project for some time, and were told that the method in which you do things needs to be changed. Are you more likely to:",
        #     "options": [
        #         ("Quickly adapt and change your approach to achieve the desired result", [3]),
        #         ("Take your time to adjust and gradually adapt to the new method", [4])
        #     ]
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
        for option, _ in q['options']:
            key = f"{q['number']}_{option}"
            confidence_value = st.session_state.get(key, "")
            confidence_intervals[option] = st.text_input(f"Confidence interval for '{option}'", value=confidence_value,
                                                         key=key, placeholder="")

        st.session_state.scorecard[q['number']] = {
            "option": selected_option,
            "choice": selected_option,
            "types": next(opt[1] for opt in q['options'] if opt[0] == selected_option),
            "confidence_intervals": confidence_intervals
        }

    if st.button("Submit All"):
        all_valid = True
        for q in questions:
            selected_option = st.session_state.scorecard[q['number']]['option']
            highest_confidence_option = max(st.session_state.scorecard[q['number']]['confidence_intervals'],
                                            key=lambda k: float(
                                                st.session_state.scorecard[q['number']]['confidence_intervals'][k]) if
                                            st.session_state.scorecard[q['number']]['confidence_intervals'][k] else 0)
            if not st.session_state.scorecard[q['number']]['confidence_intervals'][selected_option] or not (
                    0.1 <= float(
                    st.session_state.scorecard[q['number']]['confidence_intervals'][selected_option]) <= 9.9):
                all_valid = False
                st.error(
                    f"Error: Enter a confidence interval between 0.1 and 9.9 for the selected option in Question {q['number']}")
                break
            elif selected_option != highest_confidence_option:
                all_valid = False
                st.error(
                    f"Error: You must select the option with the highest confidence interval for Question {q['number']}")
                break

        if all_valid:
            for q in questions:
                selected_option = st.session_state.scorecard[q['number']]['option']
                for option, types in q['options']:
                    confidence_value = st.session_state.scorecard[q['number']]['confidence_intervals'][option]
                    if confidence_value:
                        for enneagram_type in types:
                            st.session_state.cumulative_scores[enneagram_type] += float(confidence_value)

            st.session_state.step = "results"
            st.rerun()


def show_results():
    st.title("Results")

    st.subheader("Cumulative Scores")
    st.write(st.session_state.cumulative_scores)

    dominant_type = max(st.session_state.cumulative_scores, key=st.session_state.cumulative_scores.get)
    st.subheader(f"Dominant Type: {dominant_type}")

    data = {
        "name": st.session_state.name,
        "age": st.session_state.age,
        "birthplace": st.session_state.birthplace,
        "location": st.session_state.location,
        "scorecard": st.session_state.scorecard,
        "cumulative_scores": st.session_state.cumulative_scores,
        "dominant_type": dominant_type
    }

    pickle_name = st.session_state.name.strip().lower().replace(' ', '_')
    file_name = f"{pickle_name}_responses_and_scores.pkl"

    with open(file_name, "wb") as f:
        pickle.dump(data, f)

    st.success("Your responses and scores have been saved successfully!")

    if st.button("Restart Quiz"):
        reset_session_state()


if __name__ == "__main__":
    main()
