from get_current_data_0 import get_current_data
from clean_data_1 import clean_data
from make_predictions_2 import make_predictions

get_current_data(type="player")
get_current_data(type="team")
print("get_current_data done")
clean_data(type="player")
clean_data(type="team")
print("clean_data done")
make_predictions(type="player")
make_predictions(type="team")
print("make_predictions done")
