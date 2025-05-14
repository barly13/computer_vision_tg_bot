import os
import xlwt
from io import BytesIO


class ComputerVisionReporter:
    def __init__(self):
        self.workbook = xlwt.Workbook()
        self.bytes_output = BytesIO()
        self.center_alignment_style = xlwt.easyxf("align: horiz center, vert center, wrap on; font: height 220;")
        self.header_row_style = xlwt.easyxf(
            'pattern: pattern solid, fore_colour light_green;'
            'font: bold on, height 220;'
            'align: horiz center, vert center, wrap on;'
            'borders: left medium, right medium, top medium, bottom medium;'
        )

        self.experiment_columns = [
            {
                'header': 'Номер эксперимента',
                'colspan': 1,
                'data_func': lambda data: data.get('id')
            },
            {
                'header': 'Дата',
                'colspan': 1,
                'data_func': lambda data: data.get('date')
            },
            {
                'header': 'Данные',
                'sub_columns': [
                    {
                        'header': 'Путь к файлу (реальные данные)',
                        'data_func': lambda data: data.get('real_path')
                    },
                    {
                        'header': 'Параметры генерации (сгенерированные данные)',
                        'data_func': lambda data: data.get('gen_params')
                    }
                ]
            },
            {
                'header': 'Результат (количество клеток)',
                'sub_columns': [
                    {
                        'header': 'Метод 1',
                        'data_func': lambda data: data.get('method1_result')
                    },
                    {
                        'header': 'Метод 2',
                        'data_func': lambda data: data.get('method2_result')
                    },
                    {
                        'header': 'Метод 3',
                        'data_func': lambda data: data.get('method3_result')
                    }
                ]
            }
        ]

    @staticmethod
    def __set_column_width(worksheet, column_index, value):
        min_width, max_width = 3000, 10000
        column_width = len(str(value)) * 256
        column_width = max(min_width, min(column_width, max_width))

        if worksheet.col(column_index).width < column_width:
            worksheet.col(column_index).width = column_width

    def __write_xls_header_row(self, worksheet, columns):
        column_index = 0

        for column in columns:
            if 'sub_columns' in column:
                worksheet.write_merge(0, 0, column_index, column_index + len(column['sub_columns']) - 1,
                                      column['header'], self.header_row_style)

                for sub_column_index, sub_column in enumerate(column['sub_columns']):
                    worksheet.write(1, column_index + sub_column_index, sub_column['header'], self.header_row_style)
                    self.__set_column_width(worksheet, column_index + sub_column_index, sub_column['header'])

                column_index += len(column['sub_columns'])

            else:
                worksheet.write_merge(0, 1, column_index, column_index, column['header'], self.header_row_style)
                self.__set_column_width(worksheet, column_index, column['header'])
                column_index += 1

    def __write_xls_data_row(self, worksheet, columns, row_index, data):
        column_index = 0

        for column in columns:
            if 'sub_columns' in column:
                for sub_column in column['sub_columns']:
                    value = sub_column['data_func'](data)
                    worksheet.write(row_index, column_index, value, self.center_alignment_style)
                    self.__set_column_width(worksheet, column_index, value)
                    column_index += 1

            else:
                value = column['data_func'](data)
                worksheet.write(row_index, column_index, value, self.center_alignment_style)
                self.__set_column_width(worksheet, column_index, value)
                column_index += 1

    def __generate_xls_experiment_report(self):
        try:
            worksheet = self.workbook.add_sheet('Результаты эксперимента')

            list_of_experiments = []

            self.__write_xls_header_row(worksheet, self.experiment_columns)

            for row_index, experiment in enumerate(list_of_experiments):
                self.__write_xls_data_row(worksheet, self.experiment_columns, row_index + 1, experiment)

        except Exception as exp:
            print(f'Ошибка в заполнении отчета по выполненным работам: {exp}')

    async def generate_report(self):
        self.__generate_xls_experiment_report()
        self.workbook.save(self.bytes_output)

        return self.bytes_output.getvalue()

