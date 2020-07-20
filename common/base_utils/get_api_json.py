import requests
from common.data_operation.data_get import getData
import pprint
data = getData()
row_counts = data.get_case_lines()
for row_count in range(1,row_counts):
    url = data.get_request_url(row_count)
    r = requests.get(url=f'http://ops.woda.ink/api/get_doclever_interface?url={url}')
    pprint.pprint(r.json())