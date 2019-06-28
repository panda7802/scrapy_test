import os
import sys

import django
import openpyxl
from openpyxl import Workbook

DJANGO_PROJECT_PATH = '../../lxdzx_server'
DJANGO_SETTINGS_MODULE = 'lxdzx_server.settings'
sys.path.insert(0, DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE    )
# application = django.core.handlers.wsgi.WSGIHandler()
print("===========setting over===========")
django.setup()

from dzdp.models import DzdpType


def export_types(wb):
    """
    导出类型
    :return:
    """
    types = DzdpType.objects.filter(parent_type_id=1).all()
    for item in types:
        wb.create_sheet(item.name)


def export_shops_by_type(wb, type_name):
    """
    导出商店
    :return:
    """
    pass


if __name__ == '__main__':
    print("-------start export---------")
    file_full_dir = "./res_dir"
    file_full_path = file_full_dir + "/shops.xlsx"
    # obj_file = open(file_full_path)
    # if obj_file is not None:
    #     delete()
    if not os.path.exists(file_full_path):
        if not os.path.exists(file_full_dir):
            os.makedirs(file_full_dir)

    if os.path.exists(file_full_path):
        os.remove(file_full_path)

    wb = Workbook()  # class实例化
    wb.save(file_full_path)  # 保存文件

    # 导出类型
    export_types(wb)

    def_sheet = wb.get_sheet_by_name('Sheet')
    wb.remove(def_sheet)
    wb.save(file_full_path)
