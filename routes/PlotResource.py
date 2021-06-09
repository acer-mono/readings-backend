from flask_restx import Resource
from models.Reading import Reading
from models.Room import Room
import flask_praetorian
import matplotlib.pyplot as plt
from flask import send_file
from schemas.ReadingSchema import readings_schema
from flask import request
import os
from services.utils import create_date

def get_data(arr):
    dates = []
    temps = []
    humids = []
    for item in arr:
        dates.append(create_date(item['date']))
        temps.append(item['temperature'])
        humids.append(item['humidity'])
    return dates, temps, humids


def create_humidity_temperature_plot(dates, humids, temps, start_date, end_date, room):
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
    fig.autofmt_xdate(rotation=45)
    ax1.set_title(
        'Температурно-влажностный режим в помещении "{}"\nза период с {} по {}'.format(room, start_date, end_date))
    color = 'tab:red'
    ax1.set_xlabel('Дата')
    ax1.set_ylabel('Температура', color=color)
    ax1.plot(dates, temps, marker="o", label="Температура", color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('Влажность', color=color)
    ax2.plot(dates, humids, marker="o", label="Влажность", color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    fig.savefig(os.getcwd() + '/plot.png')
    plt.close(fig)


def create_humidity_plot(dates, humids, start_date, end_date, room):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
    fig.autofmt_xdate(rotation=45)
    ax.grid(which='both')
    ax.set_title(
        'Влажностный режим в помещении "{}"\nза период с {} по {}'.format(room, start_date, end_date))
    ax.set_xlabel('Дата')

    color = 'tab:blue'
    ax.set_ylabel('Влажность', color=color)
    ax.plot(dates, humids, marker="o", label="Влажность", color=color)
    ax.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    fig.savefig(os.getcwd() + '/plot.png')
    plt.close(fig)


def create_temperature_plot(dates, temps, start_date, end_date, room):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
    fig.autofmt_xdate(rotation=45)
    ax.grid(which='both')
    ax.set_title(
        'Температурный режим в помещении "{}"\nза период с {} по {}'.format(room, start_date, end_date))
    ax.set_xlabel('Дата')

    color = 'tab:red'
    ax.set_ylabel('Температура', color=color)
    ax.plot(dates, temps, marker="o", label="Влажность", color=color)
    ax.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    fig.savefig(os.getcwd() + '/plot.png')
    plt.close(fig)


class PlotResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        try:
            start_date = request.args.get('from')
            end_date = request.args.get('to')
            room_id = request.args.get('room')
            plot_type = request.args.get('type')

            readings = readings_schema.dump(
                Reading.query.filter(Reading.date.between(start_date, end_date),
                                     Reading.room_id == room_id))
            dates, temps, humids = get_data(readings)
            room = Room.query.get(room_id)

            if plot_type == 't':
                create_temperature_plot(dates, temps, create_date(start_date), create_date(end_date), room.name)
            elif plot_type == 'h':
                create_humidity_plot(dates, humids, create_date(start_date), create_date(end_date), room.name)
            elif plot_type == 'th':
                create_humidity_temperature_plot(dates, humids, temps, create_date(start_date), create_date(end_date), room.name)
            else:
                return {'message': 'Type of the plot is not found'}, 400

            return send_file(os.getcwd() + '/plot.png',
                             attachment_filename='plot.png', as_attachment=True)
        except Exception as e:
            return {"message": str(e)}, 500
