from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
conversation_history = []


@app.route('/')
def index():
    #Display initial message asking user to click button
    initial_message = "Hello! Start by telling me if you would like either a job or internship."

    return render_template('index.html', conversation=[("Careerbot", initial_message)])


def chatbot_response(user_input):
    answer = user_input
    job = "job"
    internship = "internship"
    field = ['computer science', 'biology', 'math', 'mathematics', 'physics', 'chemistry']
    job_location = ['Suffolk', 'Norfolk', 'Newport News', 'VA Beach', 'Hampton','Cheseapeake']
    job_type = ['full-time', 'part-time', 'full time', 'part time']

    if answer in job:
        return "Great! What field do you wish to work in?"
    if answer in internship:
        return "Great! What field do you wish to work in?"
    if answer in field:
        return "Excellent choice! In which location are you searching for " + answer +  " jobs?"
    elif answer in job_location:
        return "Great! Do you want to work full-time or part-time?"
    elif answer in job_type:
        return "Here are a few jobs based on what you told me: "
    else:
        return "I'm here to assist you. Please try again."
    # Basic rule-based responses
   #if "job" in user_input.lower():
    #    return "Sure, I can help you find job listings. What type of job are you looking for?"
    #elif "internship" in user_input.lower():
     #   return "Interested in internships? Great! What field are you interested in?"
    #elif "software" in user_input.lower():
      #  return "Excellent choice! In which location are you searching for software jobs?"
    #elif "location" in user_input.lower():
     #   return "I can help you find jobs in various locations. Could you specify a city or region?"
    #else:
     #   return "I'm here to assist you. Please try again."


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

    # Get chatbot response based on user input
    bot_response = chatbot_response(user_input)

    # Update conversation history
    conversation_history.append(("User", user_input))
    conversation_history.append(("CareerBot", bot_response))

    return render_template('index.html', conversation=conversation_history)

#Handle button clicks
@app.route('/button_click', methods=['POST'])
def button_click():
    button_value = request.form['button_value']

    #Get chatbot response based on button click
    bot_response = chatbot_response(button_value)

    #Update conversation history
    conversation_history.append(("User", button_value))
    conversation_history.append(("Chatbot", bot_response))

    return render_template('index.html', conversation=conversation_history)

@app.route('/about')
def about():
    return render_template('aboutPage.html')

if __name__ == '__main__':
    app.run(debug=True)

