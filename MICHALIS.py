from tempfile import NamedTemporaryFile
import webbrowser
import pandas as pd
base_html = """
<!doctype html>
<html><head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8">
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.css">
<script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.js"></script>
</head><body>%s<script type="text/javascript">$(document).ready(function(){$('table').DataTable({
    "pageLength": 50
});});</script>
</body></html>
"""

def df_html(df):
    """HTML table with pagination and other goodies"""
    df_html = df.to_html()
    return base_html % df_html

def df_window(df):
    """Open dataframe in browser window using a temporary file"""
    with NamedTemporaryFile(delete=False, suffix='.html',mode='w+') as f:
        f.write(df_html(df))
    webbrowser.open(f.name)

df = pd.DataFrame({'a': [10, 10, 10, 11], 'b': [8, 8 ,8, 9]})
df_window(df)