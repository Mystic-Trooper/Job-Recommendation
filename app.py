from datetime import datetime
from pyvis.network import Network
import networkx as nx
from dateutil import parser
import pandas as pd

df = pd.read_json("job_descri_data.json")
jobs = df["jobs"].array

jobid = []
skills = []
year = []

counter=0

for job in jobs:
    jobid.append(job["id"])
    skills.append(job["category"])
    duration = datetime.now() - parser.parse(job["publication_date"])
    year.append(duration.seconds)
    counter+=1
    if(counter==10):
        break

kjobid = []
kskills = []


for k in range(2):
    # arbitary value to generate othe id
    kjobid.append(jobs[k]["id"]+841843278)
    kskills.append(jobs[k]["category"])


net = Network()

job_net = Network(height='1000px', width='100%',
                  bgcolor='#222222', font_color='white')

job_net.barnes_hut()
sources = jobid
targets = skills
values = year
sources_resume = kjobid
targets_resume = kskills


edge_data = zip(sources, targets, values)
resume_edge = zip(sources_resume, targets_resume)
for j, e in enumerate(edge_data):
    src = e[0]
    dst = e[1]
    w = e[2]

    job_net.add_node(src, src, color='#dd4b39', title=src)
    job_net.add_node(dst, dst, title=dst)

    if str(w).isdigit():
        if w is None:

            job_net.add_edge(src, dst, value=w, color='#00ff1e', label=w)
        if 1 < w <= 70000:
            job_net.add_edge(src, dst, value=w, color='#FFFF00', label=w)
        if w > 70000:
            job_net.add_edge(src, dst, value=w, color='#dd4b39', label=w)

    else:
        job_net.add_edge(src, dst, value=0.1, dashes=True)
for j, e in enumerate(resume_edge):
    src = 'resume'
    dst = e[1]

    job_net.add_node(src, src, color='#dd4b39', title=src)
    job_net.add_node(dst, dst, title=dst)
    job_net.add_edge(src, dst, color='#00ff1e')

neighbor_map = job_net.get_adj_list()

for node in job_net.nodes:
    node['title'] = "h1"
    node['value'] = len(neighbor_map[node['id']])
# add neighbor data to node hover data
job_net.show_buttons(filter_=['physics'])
job_net.show('knowledge_graph.html')
