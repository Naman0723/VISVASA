from flask import Flask, request, render_template, redirect, url_for #imp
import pymongo 

app = Flask(__name__) #imp
client = pymongo.MongoClient("mongodb://localhost:27017") #imp
db = client["loginPage"] #imp
collection = db["Credential"] #imp

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        contact_no = request.form['contact_no']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            message = "Passwords do not match."
            return render_template('register.html', message=message)

        existing_user = collection.find_one({"$or": [ #imp
            {"username": username}, #imp
            {"email": email}, #imp
            {"contact_no": contact_no} #imp
        ]}) #imp

        if existing_user:
            if existing_user.get("email") == email:
                message = "Email is already registered. Please use a different email."
            elif existing_user.get("username") == username:
                message = "Username is already taken. Please choose a different username."
            elif existing_user.get("contact_no") == contact_no:
                message = "Contact number is already registered. Please use a different contact number."
            return render_template('register.html', message=message)
        
        data = {
            'username': username,
            'email': email,
            'contact_no': contact_no,
            'password': password
        }
        collection.insert_one(data)
        return redirect(url_for('homepage'))

    return render_template('register.html', message=message)

@app.route('/homepage')
def homepage():
    return render_template('HOMEPAGE.html')

if __name__ == "__main__":
    app.run() 