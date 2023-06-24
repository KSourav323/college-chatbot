from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def preprocess_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    processed_text = " ".join(tokens)
    return processed_text


dataset = pd.read_csv("stud.csv", sep=",")


bot = ChatBot(
    "Terminal",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "I am sorry, but I do not understand.",
            # 'maximum_similarity_threshold': 1
        },
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter",
)

lowest_name = ""
lowest_regno = ""
topper_name = ""
topper_regno = ""
no_of_failures = 0
failures = ""
no_of_people_90 = 0
att_short = 0
no_att_short = ""
people_90 = ""


d_regno = dataset["regno"]
d_name = dataset["name"]
d_cgpa = dataset["cgpa"]
d_attendance = dataset["attendance"]
d_mobno = dataset["mobno"]
d_mail = dataset["mail"]
d_branch = dataset["branch"]
d_address = dataset["address"]
d_points = dataset["points"]
d_fee = dataset["fee"]
d_blood = dataset["blood"]

for i in range(len(d_cgpa)):
    if d_cgpa[i] == max(d_cgpa):
        topper_name = d_name[i]
        topper_regno = d_regno[i]

    if d_cgpa[i] < 6:
        no_of_failures += 1
        failures += ", " + d_name[i]

    if d_attendance[i] < 75:
        att_short += 1
        no_att_short += ", " + d_name[i]


list_trainer = ListTrainer(bot)


for i in range(0, len(d_regno)):
    # by reg_no

    list_trainer.train(
        [
            preprocess_text("complete details of {}".format(d_regno[i])),
            "Here are the details: Registeration No.: {} Name: {}  CGPA: {}  Attendance: {}  Mobile: {}  Mail Id: {}  Branch: {}  Place: {}  Activity Points: {}  Pending Fee: {}  Blood: {}".format(
                d_regno[i],
                d_name[i],
                d_cgpa[i],
                d_attendance[i],
                d_mobno[i],
                d_mail[i],
                d_branch[i],
                d_address[i],
                d_points[i],
                d_fee[i],
                d_blood[i],
            ),
        ]
    )

    list_trainer.train(
        [
            preprocess_text("what is the cgpa of {}".format(d_regno[i])),
            "Current CGPA of {} - {} is {}".format(d_regno[i], d_name[i], d_cgpa[i]),
        ]
    )

    list_trainer.train(
        [
            preprocess_text("what is the attendance of {}".format(d_regno[i])),
            "Attendance of {} - {} is {}".format(
                d_regno[i], d_name[i], d_attendance[i]
            ),
        ]
    )

    list_trainer.train(
        [
            preprocess_text("what is the mobile number of {}".format(d_regno[i])),
            "Mobile number of {} - {} is {}".format(d_regno[i], d_name[i], d_mobno[i]),
        ]
    )

    list_trainer.train(
        [
            preprocess_text("what is the mail id of {}".format(d_regno[i])),
            "Mail id of {} - {} is {}".format(d_regno[i], d_name[i], d_mail[i]),
        ]
    )

    list_trainer.train(
        [
            preprocess_text("what is the branch of {}".format(d_regno[i])),
            "Branch of {} - {} is {}".format(d_regno[i], d_name[i], d_branch[i]),
        ]
    )

    list_trainer.train(
        [
            preprocess_text("{} is from where".format(d_regno[i])),
            "{} - {} is from {}".format(d_regno[i], d_name[i], d_address[i]),
        ]
    )

    list_trainer.train(
        [
            preprocess_text("how much activity points does {} have".format(d_regno[i])),
            "{} - {} have {} points".format(d_regno[i], d_name[i], d_points[i]),
        ]
    )

    list_trainer.train(
        [
            preprocess_text("how much is the fees of {}".format(d_regno[i])),
            "Pending fees of {} - {} is {}".format(d_regno[i], d_name[i], d_mail[i]),
        ]
    )

    list_trainer.train(
        [
            preprocess_text("what is the blood group of {}".format(d_regno[i])),
            "Blood group of {} - {} is {}".format(d_regno[i], d_name[i], d_blood[i]),
        ]
    )


list_trainer.train(
    [
        preprocess_text("what is the class average"),
        "The class average is {}".format(sum(d_cgpa) / len(d_cgpa)),
    ]
)

list_trainer.train(
    [
        preprocess_text("what is the lowest cgpa"),
        "The Lowest cgpa is: {}".format(min(d_cgpa)),
    ]
)

list_trainer.train(
    [
        preprocess_text("how many failures"),
        "These many guys got below 40:  {}".format(str(no_of_failures)),
    ]
)

list_trainer.train(
    [
        preprocess_text("who all failed"),
        "These people couldn't cross 40: {}".format(failures),
    ]
)

list_trainer.train(
    [
        preprocess_text("who is the topper"),
        "The topper is {} - {} with {} cgpa".format(
            topper_name, topper_regno, max(d_cgpa)
        ),
    ]
)

list_trainer.train(
    [
        preprocess_text("attendance shortages"),
        "These students are short on attendance:  {}".format(no_att_short),
    ]
)


# while True:
#     try:
#         user_input = input('\n> ')
#         processed_input = preprocess_text(user_input)

#         response = bot.get_response(processed_input)

#         print(response)

#     except (KeyboardInterrupt, EOFError, SystemExit):
#         break
