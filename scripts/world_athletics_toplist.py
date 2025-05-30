import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns

import re
import requests
import json
from lxml import etree
from collections import namedtuple
import concurrent.futures
import itertools

from tqdm.notebook import tqdm
from IPython.display import display, HTML

base_url = "https://worldathletics.org/records/all-time-toplists"
landing_page = "/sprints/100-metres/outdoor/men/senior"
url = f"{base_url}{landing_page}"

html = requests.get(url).text
tree = etree.HTML(html)

json_compile = re.compile("toplists.init\(\\n(.*?),\\n", re.DOTALL)
element_text = "".join(
    [
        e.text
        for e in tree.xpath(".//script")
        if e.text is not None and "toplists.init" in e.text
    ]
)
matches = json_compile.search(element_text)
matches.group(1).strip()
json_dicts = json.loads(matches.group(1).strip())

# Get list of cases from json_dicts where name is disciplineCode
selected_categories, region_type = ["senior", "u20"], "world"

cases = [
    d
    for d in dict(
        *[
            json_dict
            for json_dict in json_dicts
            if json_dict["name"] == "disciplineCode"
        ]
    )["cases"]
    if d["regionType"] == region_type
    and d["ageCategory"] in selected_categories
]