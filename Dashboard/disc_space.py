import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import shutil
import io

def storage_graph():
    total, used, free = shutil.disk_usage("/")
    y = np.array([(used // (2**30)), (free // (2**30))])
    labels = ["Used GB", "Free GB"]
    fig, ax = plt.subplots()
    ax.pie(y, labels=labels, autopct=lambda p : '{:.1f} GB'.format(p * sum(y) / 100))
    ax.axis('equal')  
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf


