from dataclasses import dataclass
from enum import Enum

@dataclass
class Task:
    benchmark: str
    metric: str
    col_name: str


# Select your tasks here
# ---------------------------------------------------
class Tasks(Enum):
    # task_key in the json file, metric_key in the json file, name to display in the leaderboard 
    task0        = Task("medmcqa", "acc,none", "MedMCQA") 
    task1        = Task("medqa_4options", "acc,none", "MedQA")
    task2        = Task("mmlu_anatomy", "acc,none", "MMLU Anatomy") 
    task3        = Task("mmlu_clinical_knowledge", "acc,none", "MMLU Clinical Knowledge") 
    task4        = Task("mmlu_college_biology", "acc,none", "MMLU College Biology") 
    task5        = Task("mmlu_college_medicine", "acc,none", "MMLU College Medicine") 
    task6        = Task("mmlu_medical_genetics", "acc,none", "MMLU Medical Genetics") 
    task7        = Task("mmlu_professional_medicine", "acc,none", "MMLU Professional Medicine") 
    task8        = Task("pubmedqa", "acc,none", "PubMedQA")


    

NUM_FEWSHOT = 0 # Change with your few shot
# ---------------------------------------------------



TITLE = """


<div style="text-align: center; margin-bottom: 20px;">
    <img src="https://raw.githubusercontent.com/monk1337/MultiMedQA/main/assets/logs.png" alt="Descriptive Alt Text" style="display: block; margin: auto; height: 160px;">
</div>
<h1 align="center" style="color: #1a237e; font-size: 40px;">Open <span style="color: #990001;">Medical-LLM</span> Leaderboard</h1>


"""

# What does your leaderboard evaluate?
INTRODUCTION_TEXT = """
🩺 The Open Medical LLM Leaderboard aims to track, rank and evaluate the performance of large language models (LLMs) on medical question answering tasks. It evaluates LLMs across a diverse array of medical datasets, including MedQA (USMLE), PubMedQA, MedMCQA, and subsets of MMLU related to medicine and biology. The leaderboard offers a comprehensive assessment of each model's medical knowledge and question answering capabilities.


The datasets cover various aspects of medicine such as general medical knowledge, clinical knowledge, anatomy, genetics, and more. They contain multiple-choice and open-ended questions that require medical reasoning and understanding. More details on the datasets can be found in the "LLM Benchmarks Details" section below.


The main evaluation metric used is Accuracy (ACC). Submit a model for automated evaluation on the "Submit" page. If you have comments or suggestions on additional medical datasets to include, please reach out to us in our discussion forum.


The backend of the Open Medical LLM Leaderboard uses the Eleuther AI Language Model Evaluation Harness. More technical details can be found in the "About" page.
"""

LLM_BENCHMARKS_TEXT = f"""
<h2 style="color: #2c3e50;"> Why Leaderboard? </h2>

Evaluating the medical knowledge and clinical reasoning capabilities of LLMs is crucial as they are increasingly being applied to healthcare and biomedical applications. The Open Medical LLM Leaderboard provides a platform to assess the latest LLMs on their performance on a variety of medical question answering tasks. This can help identify the strengths and gaps in medical understanding of current models.

<h2 style="color: #2c3e50;">How it works</h2>

📈 We evaluate the models on 9 medical Q&A datasets using the <a href="https://github.com/EleutherAI/lm-evaluation-harness" target="_blank"> Eleuther AI Language Model Evaluation Harness </a>, a unified framework to test language models on different tasks.

<h2 style="color: #2c3e50;">About Open Life Science AI</h2>
An Open Life Science Project to Benchmark and Track AI Progress, Share Models and Datasets in the Life Science Field.
<a href="https://openlifescience.ai/" target="_blank"> More info </a>
<h2 style="color: #2c3e50;">Datasets</h2>

<div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;"> <ul style="list-style-type: none; padding: 0;"> <li style="margin-bottom: 20px;"> <h3 style="color: #2c3e50; margin-bottom: 5px;"><a href="https://arxiv.org/abs/2009.13081" target="_blank" style="color: #3498db;">MedQA (USMLE)</a></h3> <p>1273 real-world questions from the US Medical License Exams (USMLE) to test general medical knowledge</p> </li> <li style="margin-bottom: 20px;"> <h3 style="color: #2c3e50; margin-bottom: 5px;"><a href="https://arxiv.org/abs/1909.06146" target="_blank" style="color: #3498db;">PubMedQA</a></h3> <p>500 questions constructed from PubMed article titles along with the abstracts as context to test understanding of biomedical research</p> </li> <li style="margin-bottom: 20px;"> <h3 style="color: #2c3e50; margin-bottom: 5px;"><a href="https://proceedings.mlr.press/v174/pal22a.html" target="_blank" style="color: #3498db;">MedMCQA</a></h3> <p>4183 questions from Indian medical entrance exams (AIIMS & NEET PG) spanning 2.4k healthcare topics</p> </li> <li style="margin-bottom: 20px;"> <h3 style="color: #2c3e50; margin-bottom: 5px;"><a href="https://arxiv.org/abs/2009.03300" target="_blank" style="color: #3498db;">MMLU-Clinical knowledge</a></h3> <p>265 multiple choice questions on clinical knowledge</p> </li> <li style="margin-bottom: 20px;"> <h3 style="color: #2c3e50; margin-bottom: 5px;"><a href="https://arxiv.org/abs/2009.03300" target="_blank" style="color: #3498db;">MMLU-Medical genetics</a></h3> <p>100 MCQs on medical genetics</p> </li> <li style="margin-bottom: 20px;"> <h3 style="color: #2c3e50; margin-bottom: 5px;"><a href="https://arxiv.org/abs/2009.03300" target="_blank" style="color: #3498db;">MMLU-Anatomy</a></h3> <p>135 anatomy MCQs</p> </li> <li style="margin-bottom: 20px;"> <h3 style="color: #2c3e50; margin-bottom: 5px;"><a href="https://arxiv.org/abs/2009.03300" target="_blank" style="color: #3498db;">MMLU-Professional medicine</a></h3> <p>272 MCQs on professional medicine</p> </li> <li style="margin-bottom: 20px;"> <h3 style="color: #2c3e50; margin-bottom: 5px;"><a href="https://arxiv.org/abs/2009.03300" target="_blank" style="color: #3498db;">MMLU-College biology</a></h3> <p>144 MCQs on college-level biology</p> </li> <li> <h3 style="color: #2c3e50; margin-bottom: 5px;"><a href="https://arxiv.org/abs/2009.03300" target="_blank" style="color: #3498db;">MMLU-College medicine</a></h3> <p>173 college medicine MCQs</p> </li> </ul> </div>


<div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;"> <h2 style="color: #2c3e50;">Evaluation Metric</h2> <p>Metric Accuracy (ACC) is used as the main evaluation metric across all datasets.</p> <h2 style="color: #2c3e50;">Details and Logs</h2> <p>Detailed results are available in the results directory:</p> <a href="https://huggingface.co/datasets/openlifescienceai/results" target="_blank" style="color: #3498db;">https://huggingface.co/datasets/openlifescienceai/results</a> <p>Input/outputs for each model can be found in the details page accessible by clicking the 📄 emoji next to the model name.</p> <h2 style="color: #2c3e50;">Reproducibility</h2> <p>To reproduce the results, you can run this evaluation script:</p> <pre style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">python eval_medical_llm.py</pre> <p>To evaluate a specific dataset on a model, use the EleutherAI LLM Evaluation Harness:</p> <pre style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">python main.py --model=hf-auto --model_args="pretrained=&lt;model&gt;,revision=&lt;revision&gt;,parallelize=True" --tasks=&lt;dataset&gt; --num_fewshot=&lt;n_shots&gt; --batch_size=1 --output_path=&lt;output_dir&gt;</pre> <p>Note some datasets may require additional setup, refer to the Evaluation Harness documentation.</p> <p>Adjust batch size based on your GPU memory if not using parallelism. Minor variations in results are expected with different batch sizes due to padding.</p> <h2 style="color: #2c3e50;">Icons</h2> <ul style="list-style-type: none; padding: 0;"> <li>🟢 Pre-trained model</li> <li>🔶 Fine-tuned model</li> <li>? Unknown model type</li> <li>⭕ Instruction-tuned</li> <li>🟦 RL-tuned</li> </ul> <p>Missing icons indicate the model info is not yet added, feel free to open an issue to include it!</p> </div>
"""

LLM_BENCHMARKS_DETAILS = f"""
Datasets
<a href="https://arxiv.org/abs/2009.13081" target="_blank">MedQA (USMLE)</a> - 1273 real-world questions from the US Medical License Exams (USMLE) to test general medical knowledge
<a href="https://arxiv.org/abs/1909.06146" target="_blank">PubMedQA</a> - 500 questions constructed from PubMed article titles along with the abstracts as context to test understanding of biomedical research
<a href="https://proceedings.mlr.press/v174/pal22a.html" target="_blank">MedMCQA</a> - 4183 questions from Indian medical entrance exams (AIIMS & NEET PG) spanning 2.4k healthcare topics
<a href="https://arxiv.org/abs/2009.03300" target="_blank">MMLU-Clinical knowledge</a> - 265 multiple choice questions on clinical knowledge
<a href="https://arxiv.org/abs/2009.03300" target="_blank">MMLU-Medical genetics</a> - 100 MCQs on medical genetics
<a href="https://arxiv.org/abs/2009.03300" target="_blank">MMLU-Anatomy</a> - 135 anatomy MCQs
<a href="https://arxiv.org/abs/2009.03300" target="_blank">MMLU-Professional medicine</a> - 272 MCQs on professional medicine
<a href="https://arxiv.org/abs/2009.03300" target="_blank">MMLU-College biology</a> - 144 MCQs on college-level biology
<a href="https://arxiv.org/abs/2009.03300" target="_blank">MMLU-College medicine</a> - 173 college medicine MCQs
Metric
Accuracy (ACC) is used as the main evaluation metric across all datasets
Details and logs
Detailed results are available in the results directory: https://huggingface.co/spaces/openlifescienceai/open_medical_llm_leaderboard/tree/main/results
Input/outputs for each model can be found in the details page accessible by clicking the 📄 emoji next to the model name
Reproducibility
To reproduce the results, you can run this evaluation script: python eval_medical_llm.py.
To evaluate a specific dataset on a model, use the EleutherAI LLM Evaluation Harness:
python main.py --model=hf-auto --model_args="pretrained=<model>,revision=<revision>,parallelize=True"
 --tasks=<dataset> --num_fewshot=<n_shots> --batch_size=1 --output_path=<output_dir>
Note some datasets may require additional setup, refer to the Evaluation Harness documentation. Adjust batch size based on your GPU memory if not using parallelism. Minor variations in results are expected with different batch sizes due to padding.
Icons
🟢 Pre-trained model
🔶 Fine-tuned model
? Unknown model type
⭕ instruction-tuned
🟦 RL-tuned
Missing icons indicate the model info is not yet added, feel free to open an issue to include it!
"""

FAQ_TEXT = """
FAQ
1) Submitting a model
XXX
2) Model results
XXX
3) Editing a submission
XXX
"""

EVALUATION_QUEUE_TEXT = """
Evaluation Queue for the Open Medical LLM Leaderboard
Models added here will be automatically evaluated.

Before submitting a model
1) Verify loading with AutoClasses:


from transformers import AutoConfig, AutoModel, AutoTokenizer
config = AutoConfig.from_pretrained("model-name", revision=revision) 
model = AutoModel.from_pretrained("model-name", revision=revision)

tokenizer = AutoTokenizer.from_pretrained("model-name", revision=revision)
Debug any loading errors before submission. Make sure the model is public.

Note: Models that require use_remote_code=True are not yet supported.

2) Convert weights to safetensors
This allows faster loading and enables showing model parameters in the Extended Viewer.

3) Select correct precision
Incorrect precision (e.g. loading bf16 as fp16) can cause NaN errors for some models.

Debugging failing models
For models in FAILED status, first ensure the above checks are done.

Then test running the Eleuther AI Harness locally using the command in the "Reproducibility" section, specifying all arguments. Add --limit to evaluate on fewer examples per task.
"""

CITATION_BUTTON_LABEL = "Copy the citation snippet"
CITATION_BUTTON_TEXT = r"""
@misc{openlifescienceai/open_medical_llm_leaderboard,
author = {Ankit Pal, Pasquale Minervini and Andreas Geert Motzfeldt},
title = {openlifescienceai/open_medical_llm_leaderboard},
year = {2024},
publisher = {Hugging Face},
howpublished = "\url{https://huggingface.co/spaces/openlifescienceai/open_medical_llm_leaderboard}"
}
@misc{singhal2022large,
      title={Large Language Models Encode Clinical Knowledge}, 
      author={Karan Singhal et al.},
      year={2022},
      eprint={2212.13138},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""
