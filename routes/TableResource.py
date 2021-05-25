from models.Reading import Reading
from flask_restx import Resource
from schemas.ReadingSchema import readings_schema
import flask_praetorian
from fpdf import FPDF
from flask import Response
from flask import request
import xlsxwriter
import io
import csv
import mimetypes
from services.utils import create_date
from werkzeug.datastructures import Headers

DATE_HEADER = "Дата"
TEMPERATURE_HEADER = "Температура"
HUMIDITY_HEADER = "Влажность"


def create_pdf(readings):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)
    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('DejaVu', 'B', 12)

    col_width = page_width / 3

    th = pdf.font_size + 2
    pdf.cell(col_width, th, DATE_HEADER, border=1, align='C')
    pdf.cell(col_width, th, TEMPERATURE_HEADER, border=1, align='C')
    pdf.cell(col_width, th, HUMIDITY_HEADER, border=1, align='C')
    pdf.ln(th)

    pdf.set_font('DejaVu', '', 12)

    for row in readings:
        pdf.cell(col_width, th, create_date(row['date']), border=1)
        pdf.cell(col_width, th, str(row['temperature']), border=1)
        pdf.cell(col_width, th, str(row['humidity']), border=1)
        pdf.ln(th)

    pdf.ln(10)

    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=employee_report.pdf'})


def create_xlsx(readings):
    response = Response()
    response.status_code = 200

    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('data')

    row = 0
    col = 0
    worksheet.write(row, col, DATE_HEADER)
    worksheet.write(row, col + 1, TEMPERATURE_HEADER)
    worksheet.write(row, col + 2, HUMIDITY_HEADER)
    row += 1

    for reading in readings:
        worksheet.write(row, col, create_date(reading['date']))
        worksheet.write(row, col + 1, reading['temperature'])
        worksheet.write(row, col + 2, reading['humidity'])

    workbook.close()

    output.seek(0)

    response.data = output.read()

    file_name = 'table.xlsx'
    mimetype_tuple = mimetypes.guess_type(file_name)

    response_headers = Headers({
        'Pragma': "public",
        'Expires': '0',
        'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
        'Cache-Control': 'private',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'Content-Disposition': 'attachment; filename=\"%s\";' % file_name,
        'Content-Transfer-Encoding': 'binary',
        'Content-Length': len(response.data)
    })

    if not mimetype_tuple[1] is None:
        response.update({
            'Content-Encoding': mimetype_tuple[1]
        })

    response.headers = response_headers

    return response


def create_csv(readings):
    si = io.StringIO()
    cw = csv.writer(si)

    cw.writerow(list([DATE_HEADER, TEMPERATURE_HEADER, HUMIDITY_HEADER]))
    for i in readings:
        cw.writerow([create_date(i['date']), i['temperature'], i['humidity']])
    return Response(si.getvalue(),
                    mimetype="text/csv",
                    headers={'Content-Disposition': 'attachment; filename=table.csv'})


TABLE_CREATOR = {
    'pdf': create_pdf,
    'xlsx': create_xlsx,
    'csv': create_csv
}


class TableResource(Resource):
    @flask_praetorian.auth_required
    def get(self):
        try:
            start_date = request.args.get('from')
            end_date = request.args.get('to')
            room_id = request.args.get('room')

            readings = readings_schema.dump(
                Reading.query.filter(Reading.date.between(start_date, end_date),
                                     Reading.room_id == room_id))
            f = request.args.get('format')

            return TABLE_CREATOR[f](readings)
        except Exception as e:
            return {"message": str(e)}, 500
