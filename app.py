from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def patients():

    patients = [
        {
            "name": "Alexander, Elizabeth",
            "dob": "2/23/1951",
            "mrn": "548001",
            "account": "100145324",
            "encounter": "Emergency",
            "facility": "Jackson Street Hospital Campus",
            "discharge": "8/31/2026 10:17 AM",
            "tasks": "2",
            "pcp": "Dr. Wilson",
            "payer": "SILVER HEALTHCARE"
        },
        {
            "name": "Brianna, Harrell",
            "dob": "9/22/1993",
            "mrn": "448002",
            "account": "1001453246",
            "encounter": "Emergency",
            "facility": "Jackson Street Hospital Campus",
            "discharge": "8/31/2026 07:37 AM",
            "tasks": "1",
            "pcp": "Dr. Smith",
            "payer": "GOLD HEALTHCARE"
        },
        {
            "name": "Cabrera, Francisco",
            "dob": "6/30/1958",
            "mrn": "4437923",
            "account": "1001453245",
            "encounter": "Emergency",
            "facility": "Jackson Street Hospital Campus",
            "discharge": "8/31/2026 07:18 AM",
            "tasks": "0",
            "pcp": "Dr. Garcia",
            "payer": "SILVER PPO"
        },
        {
            "name": "Nunnally, David",
            "dob": "7/06/1949",
            "mrn": "435754",
            "account": "1001453243",
            "encounter": "Emergency",
            "facility": "Jackson Street Hospital Campus",
            "discharge": "8/31/2026 06:49 AM",
            "tasks": "3",
            "pcp": "Dr. Johnson",
            "payer": "BLUE CROSS BLUE SHIELD PPO"
        },
        {
            "name": "Atienza, Aiden",
            "dob": "5/28/2004",
            "mrn": "413723",
            "account": "1001453241",
            "encounter": "Emergency",
            "facility": "Jackson Street Hospital Campus",
            "discharge": "8/31/2026 06:35 AM",
            "tasks": "1",
            "pcp": "Dr. Thompson",
            "payer": "UNITED HEALTHCARE"
        },
        {
            "name": "Thomas, Jayson",
            "dob": "2/02/2012",
            "mrn": "448601",
            "account": "1001453240",
            "encounter": "Emergency",
            "facility": "Jackson Street Hospital Campus",
            "discharge": "8/31/2026 06:23 AM",
            "tasks": "2",
            "pcp": "Dr. Harris",
            "payer": "TX CHILDREN'S MEDICAID"
        },
        {
            "name": "Luna, Lionel",
            "dob": "2/10/1963",
            "mrn": "446749",
            "account": "1001453223",
            "encounter": "Emergency",
            "facility": "Jackson Street Hospital Campus",
            "discharge": "8/31/2026 06:37 AM",
            "tasks": "1",
            "pcp": "Dr. Garcia",
            "payer": "WELLMOUNT MEDICARE"
        },
        {
            "name": "Ramirez, Olga",
            "dob": "9/10/1989",
            "mrn": "415715",
            "account": "1001453208",
            "encounter": "Emergency",
            "facility": "Jackson Street Hospital Campus",
            "discharge": "8/31/2026 02:53 AM",
            "tasks": "1",
            "pcp": "Dr. Mitchell",
            "payer": "SILVER PPO"
        }
    ]

    return render_template(
        "patients.html",
        patients=patients
    )


if __name__ == "__main__":
    app.run(debug=True)