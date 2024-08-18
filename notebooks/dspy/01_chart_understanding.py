import base64
import io
import requests

import weave
from datasets import load_dataset
from tqdm.auto import tqdm


weave.init(project_name="geekyrakshit/dspy-visit-bench")
dataset = load_dataset("mlfoundations/VisIT-Bench")["test"].to_list()

weave_dataset = []
for idx in tqdm(range(len(dataset))):
    encoded_string = base64.b64encode(
        io.BytesIO(requests.get(dataset[idx]["image"]["path"]).content).getvalue()
    ).decode("utf-8")
    dataset[idx]["image"] = f"data:image/png;base64,{encoded_string}"
    weave_dataset.append(dataset[idx])

weave_dataset_reference = weave.publish(
    weave.Dataset(name="VisIT-Bench", rows=weave_dataset)
)
