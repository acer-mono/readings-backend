from flask_restx import Resource
from models.Reading import Reading
from flask_jwt_extended import jwt_required
import matplotlib.pyplot as plt
from flask import send_from_directory

def getTemperature(arr):
    dates = []
    temps = []
    humids = []
    for item in arr:
        dates.append(item['date'])
        temps.append(item['temperature'])
        humids.append(item['humidity'])
    return dates, temps, humids

class PlotResource(Resource):
    @jwt_required()
    def get(self):
        fig, ax = plt.subplots(nrows=1, ncols=1)
        readings = Reading.query.all()
        dates, temps, humids = getTemperature(readings)
        ax.plot(dates, temps)
        fig.savefig('./plot.png')
        plt.close(fig)
        return send_from_directory('./', 'to.png', as_attachment=True)