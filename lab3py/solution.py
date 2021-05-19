from data_reader import read_data, get_goals

class ID3:

    data = []

    def __init__(self):
        pass

    def fit(self, data):
        pass

    def predict(self, data):
        pass
    

def main():
    filename = r'lab3_files[8]\datasets\volleyball.csv'
    data = read_data(filename)
    goals = get_goals(data[1])

    print('data: ', data)
    print('goals: ', goals)


    
if __name__ == '__main__':
    main()