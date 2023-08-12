from flask import Flask,render_template,request,redirect
from secrets import compare_digest
import json
import pandas as pd
import os

app = Flask(__name__)

is_user_logged=False
is_seller_logged = False
seller_user_name = ''
user_name = ''

app.config['UPLOAD_FOLDER'] = 'static/images'
app.secret_key = 'abcdefg'


@app.route("/under_construction")
def un_cons():
    return render_template("udnder_construction.html")



@app.route("/")
def main():
    global user_name
    global is_user_logged
    if is_user_logged:
        U_name = user_name
    else:
        U_name = 'Sign In'
    return render_template('index.html',name = U_name)


#login credentials


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/validate", methods=['GET','POST'])
def user_validate():

    global user_name
    global is_user_logged
    username = request.form['user_name']
    password = request.form['passwd']

    with open("static/customer_login_cred.json") as dat_file:
        data = json.load(dat_file)

        names = data['Name']

        n_list = [data for data in names]

        names_list = [names[d] for d in n_list]
        if username in names_list:
            user_name += username
            is_user_logged = True
            return redirect("/")
        else:
            return 'eror'

@app.route("/seller_login")
def seller_login():
    global is_seller_logged
    global seller_user_name
    if is_seller_logged:
        return render_template("seller_page.html", name=seller_user_name)
    else:
        return render_template("seller_login.html")

@app.route("/seller_validate",methods=['GET','POST'])
def seller_validate():
    global seller_user_name
    global is_seller_logged
    username = request.form['user_name']
    password = request.form['passwd']

    with open("static/seller_login_cred.json") as dat_file:
        data = json.load(dat_file)

        names = data['Name']

        n_list = [data for data in names]

        names_list = [names[d] for d in n_list]

        if username in names_list:
            seller_user_name += username
            is_seller_logged =True
            return render_template("seller_page.html",name=seller_user_name)
        else:
            return 'eror'

# register new account

@app.route("/Register")
def register():
    global is_user_logged
    is_user_logged = False
    return render_template("regsiter.html")

@app.route("/registering",methods=['GET','POST'])
def registering_data():
    if request.method=='POST':
        name = request.form['name']
        ph_no = request.form['ph_no']
        w_r_u = request.form['who are you']
        psd_1 = request.form['paswd_1']
        psd_2 = request.form['paswd_2']
        if psd_1 == psd_2:
            if w_r_u=='Customer':
                with open('static/customer_login_cred.csv','a') as data_file:
                    data_file.write(f"\n{name},{ph_no},{w_r_u},{psd_1},{psd_2}")

                df = pd.read_csv("static/customer_login_cred.csv")

                data = df.to_dict()

                with open('static/customer_login_cred.json','w') as data_file:
                    json.dump(data,data_file,indent=4)
            elif w_r_u == 'Seller':
                with open('static/seller_login_cred.csv','a') as data_file:
                    data_file.write(f"\n{name},{ph_no},{w_r_u},{psd_1},{psd_2}")

                df = pd.read_csv("static/seller_login_cred.csv")

                data = df.to_dict()

                with open('static/seller_login_cred.json','w') as data_file:
                    json.dump(data,data_file,indent=4)

            return redirect('/')
        else:
            return redirect("/Register")
@app.route("/User")
def user_account():
    global user_name

    return render_template('user.html',user_name = user_name)


#product listing page

# vegetables listing
@app.route("/Vegetables")
def Vegetables():
    product_name='Vegetables'

    # with open('static/vegetables/vegetables.csv') as data_file:
    #     data = data_file.read()
    df = pd.read_csv('static/vegetables/vegetables.csv')
    data = df.to_dict()
    with open('static/vegetables/vegetables.json','w') as data_file:
        json.dump(data,data_file,indent=4)
    with open('static/vegetables/vegetables.json') as data_file:
        data = json.load(data_file)
    return render_template("Product_listing.html",p_name=product_name,d=data)

# fruits listing
@app.route("/Fruits")
def Fruits():
    product_name='Fruits'
    df = pd.read_csv('static/Fruits/Fruits.csv')
    data = df.to_dict()
    with open('static/Fruits/Fruits.json', 'w') as data_file:
        json.dump(data, data_file, indent=4)
    with open('static/Fruits/Fruits.json') as data_file:
        data = json.load(data_file)
    return render_template("Product_listing.html",p_name=product_name,d=data)

# cereal crops listing
@app.route("/Cereal+Crops")
def Cereal_Crops():
    product_name = 'Fruits'
    df = pd.read_csv('static/Cereal_Crops/cereal_crops.csv')
    data = df.to_dict()
    with open('static/Cereal_Crops/cereal_crops.json', 'w') as data_file:
        json.dump(data, data_file, indent=4)
    with open('static/Cereal_Crops/cereal_crops.json') as data_file:
        data = json.load(data_file)
    return render_template("Product_listing.html", p_name=product_name,d=data)

# sunday's plan listing
@app.route("/Sunday'+Plan")
def sunday_plan():
    product_name = "Sunday's Plan"
    df = pd.read_csv("static/Sunday's_plan/Sunday's_Plan.csv")
    data = df.to_dict()
    with open("static/Sunday's_plan/Sunday's_Plan.json", 'w') as data_file:
        json.dump(data, data_file, indent=4)
    with open("static/Sunday's_plan/Sunday's_Plan.json") as data_file:
        data = json.load(data_file)
    return render_template("Product_listing.html", p_name=product_name, d=data)


# search results
@app.route("/Search",methods=['POST','GET'])
def search():
    if request.method=='POST':
        n = request.form['query']
        if n == 'Vegetables' or n=='vegetables':
            return redirect('/Vegetables')
        elif n == 'Rice' or n == 'rice' or n== 'Wheat' or n=='wheat' or n == 'nuts' or n == 'Nuts' or n == 'cereals crops' or n == 'Cereals crops':
            return redirect('/Cereal+Crops')
        elif n == 'Fruits' or n == 'fruits':
            return redirect('/Fruits')
        return redirect('/under_construction')


## add to cart
@app.route("/Cart")
def cart():
    return render_template('cart.html')

## buy's the product
@app.route("/buying the product")
def buy_product():

    return render_template("all_buying.html")



#seller upload produce
@app.route("/update_seller_produce",methods=['POST','GET'])
def update_seller_produce():
    global seller_user_name
    if request.method=='POST':
        prod_name = request.form['prod_name']
        price = request.form['prod_price']
        img = request.files['images']
        cate = request.form['cate']
        if img.filename != '':
            image_path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
            img.save(image_path)

        with open(f'static/user_data/user_data.csv','a') as datafile:
            datafile.write(f'\n{prod_name},{price},static/images/{img.filename},{cate}')

        if cate == 'Vegetables':
            with open('static/vegetables/vegetables.csv', 'a') as data_file:
                data_file.write(f'\n{prod_name},{price},static/images/{img.filename}')

        elif cate == 'Fruits':
            with open('static/Fruits/Fruits.csv', 'a') as data_file:
                data_file.write(f'\n{prod_name},{price},static/images/{img.filename}')

        elif cate == 'Cereal_crops':
            with open('static/Cereal_Crops/cereal_crops.csv', 'a') as data_file:
                data_file.write(f'\n{prod_name},{price},static/images/{img.filename}')

        return redirect('/')
    else:
        return 'error'



# seller produce upload
@app.route("/Upload_Your_Produce")
def upload_your_produce():
    return render_template('seller_produce_uploade.html')

@app.route("/seller_history")
def seller_history():


    df = pd.read_csv('static/user_data/user_data.csv')

    data = df.to_dict()

    with open('static/user_data/user_data.json', 'w') as datafile:
        json.dump(data, datafile,indent=4)

    with open('static/user_data/user_data.json') as datafile:
        data = json.load(datafile)

    return render_template('seller_fistory.html',data = data)


@app.route("/update_farm_id")
def Update_Farm_Id():
    return render_template("Update_Farm_Id.html")

@app.route("/validate_farm_id",methods=['POST','GET'])
def validate_farm_id():
    if request.method=='POST':
        return redirect('/')
    else:
        return '<center><h2>404 error</h2></center>'

##notification user account
@app.route("/notification_from_admin")
def noti_from_admin():
    return render_template("noti_from_admin.html")


##exit code
@app.route("/exit_web")
def exit_web():
    global is_user_logged
    global user_name
    global is_seller_logged
    global seller_user_name
    is_user_logged = False
    is_seller_logged = False
    seller_user_name =''
    user_name =''
    return redirect('/')





if __name__=="__main__":
    app.run(debug=True,port=2307)