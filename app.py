from flask import Flask,render_template,request
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms

from get_match import get_random_match


app = Flask(__name__)
class DataStore():
    match = None
    you=0
    ann=0

stored = DataStore()
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(52, 64)
        self.fc2 = nn.Linear(64,64)
        self.fc3 = nn.Linear(64,64)
        self.fc4 = nn.Linear(64,2)
    
    def forward(self,x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.softmax(self.fc4(x),dim=1)
        return x

def predict(match, given):
    X=match[:-1]
    X=[float(i) for i in X]
    X_tensor = torch.FloatTensor(X)
    Y=match[-1:]
    Y_tensor=torch.FloatTensor(Y)
    model = torch.load('./updated_weights.h5')
    X_tensor = X_tensor.view(-1,X_tensor.shape[0])
    print(X_tensor.shape)

    you=0
    ann=0
    #model.zero_grad()
    with torch.no_grad():
        res=""
        output = model(X_tensor.float())
        print("JAJA",Y_tensor[0])
        if(int(given)!=Y_tensor):
            res+="YOU WERE WRONG and "
        else:
            res+="YOU ARE RIGHT and"
            stored.you+=1
            
        if((Y_tensor==0 and output[0][0] > output[0][1]) or (Y_tensor==1 and output[0][0] < output[0][1])):
            res+=" THE NETWORK GOT IT RIGHT"
            stored.ann+=1
        else:
            res+=" THE NETWORK GOT IT WRONG"
        return (res,you,ann,)


@app.route("/",methods=['GET', 'POST'])
def home():
    data = get_random_match()
    teams = data[1]
    match = data[0]
    stored.match = match
    
    print("CRCTED", match)
    return render_template("index.html",t=teams,you=stored.you,ann=stored.ann)


@app.route("/predict",methods=['GET','POST'])
def result():
    a = request.form['team']
    match = stored.match
    print("AKG",stored.match)
    res = predict(match,a)
    print(res)
   
    print("team ",str(a)," won")
    return render_template("predict.html",result=res[0])

    
if __name__ == "__main__":
    app.run(debug=True)