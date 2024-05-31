# imports
import os
import json
import numpy as np

# Import torch
import torch
import torch.nn as nn
import torch.optim as optim

#Sample data
path_dir = os.path.dirname(__file__)
with open(os.path.join(path_dir, 'timeseries_pheno_metrics.json')) as f:
    json = json.load(f)

X_train = json["timeseries_pheno_metrics"]
y_train = json["label_id"]

#Convert data to PyTorch tensors
X_train_tensor = torch.tensor(np.expand_dims(X_train, axis=1), dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)

print(X_train_tensor.shape)

#LSTM classifier model
class LSTMClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMClassifier, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

#Define model parameters
input_size = X_train_tensor.shape[2]
hidden_size = 64
num_layers = 2
output_size = len(set(y_train_tensor))

#Instantiate
model = LSTMClassifier(input_size, hidden_size, num_layers, output_size)

#Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

#Train the model
num_epochs = 1000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}')

#Making prediction
from cshd import cube_query, get_timeseries, params_phenometrics, calc_phenometrics, cshd_array

def return_class_by_id(id):
    if 370: return "Soja"
    if 372: "Arroz"
    if 359: "Vegetação Florestal"
    if 365: "Corpos d'agua"
    if 367: return "Superfícies Artificiais"
    if 363: return "Pastagem"
    if 361: return "Formação Campestre"

S2_cube = cube_query(
    collection="S2-16D-2",
    start_date="2023-01-01",
    end_date="2023-12-31",
    freq='16D',
    band="NDVI"
)

config = params_phenometrics(
    peak_metric='pos', 
    base_metric='vos', 
    method='seasonal_amplitude', 
    factor=0.2, 
    thresh_sides='two_sided', 
    abs_value=0.1
)

longitude = -52.97612606396396
latitude =  -29.325361867915753

ts = get_timeseries(
    cube=S2_cube, 
    geom=[dict(coordinates = [longitude, latitude])],
    cloud_filter = True
)
ndvi_array = cshd_array(
    timeserie=ts['values'],
    start_date='2023-01-01',
    freq='16D'
)
ds_phenos = calc_phenometrics(
    da=ndvi_array,
    engine='phenolopy',
    config=config,
    start_date='2023-01-01'
)
test_tl = ts['values'] + ds_phenos

X_test_tensor = torch.tensor(np.expand_dims([test_tl], axis=1), dtype=torch.float32)
with torch.no_grad():
    predictions = model(X_test_tensor)
    predicted_labels = torch.argmax(predictions, dim=1)
    print("Predicted Label:", predicted_labels[0], return_class_by_id(predicted_labels[0]))