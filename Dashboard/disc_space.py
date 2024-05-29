from matplotlib.figure import Figure
import numpy as np
import shutil
import base64
import io

#matplotlib.use('Agg')

def storage_graph(directory):
    total, used, free = shutil.disk_usage(directory)
    y = np.array([(used // (2**30)), (free // (2**30))])
    labels = ["Used GB", "Free GB"]

    fig =  Figure()

    ax = fig.subplots()
    ax.pie(y, labels=labels, autopct=lambda p : '{:.1f} GB'.format(p * sum(y) / 100))
    ax.axis('equal')  
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    
    img = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img


