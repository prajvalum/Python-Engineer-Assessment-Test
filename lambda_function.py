import xlrd
import json
import boto3

def process_sheet(file_path, read_field):
    read_obj = xlrd.open_workbook(file_path)
    tab_index = read_obj.sheet_names().index(read_field)
    sheet_obj = read_obj.sheet_by_index(tab_index) 
    result_json = {}
    for column_index in range(0, sheet_obj.ncols):
        column_name  = sheet_obj.cell(0, column_index).value
        result_json[column_name] = []
        for row_index in range(1, sheet_obj.nrows):
            row_value = sheet_obj.cell(row_index, column_index).value
            result_json[column_name].append(row_value)
    return json.dumps(result_json)

def save_to_s3_bucket(data):
    AWS_BUCKET_NAME = "prajval"
    s3 = boto3.resource("s3")
    path = 'list_by_cc.json'
    obj = s3.Object(AWS_BUCKET_NAME, path)
    obj.put(Body=data)
    body = {
        "uploaded": "true",
        "bucket": AWS_BUCKET_NAME,
        "path": path
    }
    return {
        "statusCode": 200,
        "body": body
    }
 
def lambda_handler(event, context):
    file_path = "ISO10383_MIC.xls"
    read_field = "MICs List by CC"
    result_json = process_sheet(file_path, read_field)
    result = save_to_s3_bucket(result_json)
    return result

