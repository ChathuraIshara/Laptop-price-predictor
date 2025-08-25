from flask import Flask, render_template, request, redirect, url_for
import pickle

app = Flask(__name__)

def prediction(lst):
    filename = 'model/predictor.pickle';
    with open(filename,'rb') as file:
        model = pickle.load(file)
        pred_value =  model.predict([lst])
        return pred_value;


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')

        featureList = []
        featureList.append(int(ram))
        featureList.append(float(weight))
        featureList.append(len(touchscreen))
        featureList.append(len(ips))

        company_list = ['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
        typename_list = ['2in1convertible','gaming','netbook','notebook','ultrabook','workstation']
        opsys_list = ['linux','mac','other','windows']
        cpu_list = ['amd','intelcorei3','intelcorei5','intelcorei7','other']
        gpu_list = ['amd','intel','nvidia']

        def tranversList(lst, value):
            for item in lst:
                if item == value:
                    featureList.append(1)
                else:
                    featureList.append(0)
        tranversList(company_list, company)
        tranversList(typename_list, typename)
        tranversList(opsys_list, opsys)
        tranversList(cpu_list, cpu)
        tranversList(gpu_list, gpu)

        pred = prediction(featureList)
        pred_value = round(float(pred[0]) * 219, 2)
        print(f'Predicted Price is {pred_value}')
        return redirect(url_for('index', pred=pred_value))

    # GET request
    pred = request.args.get('pred', default=0, type=float)
    return render_template('index.html', pred=pred)


if __name__ == '__main__':
    app.run(debug=True)