from angledata import smoothed_df, phase_divider, grab_label

# class to get data from user or professional 
class Player_data:
    def __init__(self, path, angle, name):
        self.path = path
        self.angle = angle
        self.name = name
    
    def get_data(self):
        data = smoothed_df(self.path, self.angle)
        return data

    def doughnut(self):
        doughnut_data = phase_divider(self.path)
        return doughnut_data

    def labels(self):
        labels = grab_label(self.path, self.angle)
        return labels


#djok = Pro_data('pose/data/serve_data/djokserve45.csv', 'hip2ankle_right', 'Djokovic')



