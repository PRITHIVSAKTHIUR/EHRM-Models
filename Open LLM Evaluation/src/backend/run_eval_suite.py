# import json
# import os
# import logging
# from datetime import datetime

# from lm_eval import tasks, evaluator, utils

# from src.envs import RESULTS_REPO, API
# from src.backend.manage_requests import EvalRequest

# logging.getLogger("openai").setLevel(logging.WARNING)

# def run_evaluation(eval_request: EvalRequest, task_names, num_fewshot, batch_size, device, local_dir: str, results_repo: str, no_cache=True, limit=None):
#     if limit:
#         print(
#             "WARNING: --limit SHOULD ONLY BE USED FOR TESTING. REAL METRICS SHOULD NOT BE COMPUTED USING LIMIT."
#         )
#     task_names = ["medmcqa", "medqa_4options", "mmlu_anatomy", "mmlu_clinical_knowledge", "mmlu_college_biology", "mmlu_college_medicine", "mmlu_medical_genetics", "mmlu_professional_medicine", "pubmedqa"]

#     print(f"Selected Tasks: {task_names}")
#     results = evaluator.simple_evaluate(
#         model="hf-causal-experimental", # "hf-causal"
#         model_args=eval_request.get_model_args(),
#         tasks=task_names,
#         # num_fewshot=num_fewshot,
#         batch_size=batch_size,
#         device=device,
#         no_cache=no_cache,
#         limit=limit,
#         write_out=True,
#         output_base_path="logs"
#     )

#     results["config"]["model_dtype"] = eval_request.precision
#     results["config"]["model_name"] = eval_request.model
#     results["config"]["model_sha"] = eval_request.revision

#     dumped = json.dumps(results, indent=2)
#     print(dumped)

#     output_path = os.path.join(local_dir, *eval_request.model.split("/"), f"results_{datetime.now()}.json")
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)
#     with open(output_path, "w") as f:
#         f.write(dumped)

#     print(evaluator.make_table(results))

#     API.upload_file(
#         path_or_fileobj=output_path,
#         path_in_repo=f"{eval_request.model}/results_{datetime.now()}.json",
#         repo_id=results_repo,
#         repo_type="dataset",
#     )

#     return results

import json
import os
import logging
from datetime import datetime

from lm_eval import tasks, evaluator, utils
import requests

from src.envs import RESULTS_REPO, API
from src.backend.manage_requests import EvalRequest

logging.getLogger("openai").setLevel(logging.WARNING)

def run_evaluation(eval_request: EvalRequest, task_names, num_fewshot, batch_size, device, local_dir: str, results_repo: str, no_cache=True, limit=None):
    if limit:
        print(
            "WARNING: --limit SHOULD ONLY BE USED FOR TESTING. REAL METRICS SHOULD NOT BE COMPUTED USING LIMIT."
        )
    task_names = ["medmcqa", "medqa_4options", "mmlu_anatomy", "mmlu_clinical_knowledge", "mmlu_college_biology", "mmlu_college_medicine", "mmlu_medical_genetics", "mmlu_professional_medicine", "pubmedqa"]

  
    print(f"Selected Tasks: {task_names}")

    url = os.environ.get("URL")

    data = {"args": f"pretrained={eval_request.model}"}
    print("datasending", data)
    response = requests.post(url, json=data)
    print("response, response", response)
    results_full = {'results': {}, 'config': {}}

    # url = os.environ.get("URL")

    # headers = {
    # 'bypass-tunnel-reminder': 'anyvalue'
    # }
    
    # data = {"args": f"pretrained={eval_request.model}"}
    # print("datasending", data)
    # response = requests.post(url, json=data, headers=headers)
    # print("response, response", response)
    # results_full = {'results': {}, 'config': {}}

    results_full['results'] = response.json()['result']['results']
    results_full["config"]["model_dtype"] = eval_request.precision
    results_full["config"]["model_name"] = eval_request.model
    results_full["config"]["model_sha"] = eval_request.revision

    dumped = json.dumps(results_full, indent=2)
    # print(dumped)

    output_path = os.path.join(local_dir, *eval_request.model.split("/"), f"results_{datetime.now()}.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(dumped)

    # print(evaluator.make_table(results_full))

    API.upload_file(
        path_or_fileobj=output_path,
        path_in_repo=f"{eval_request.model}/results_{datetime.now()}.json",
        repo_id=results_repo,
        repo_type="dataset",
    )

    return results_full