import os
import re
import sys
import json
import tempfile
import gradio as gr

from transformers import (
    TrainingArguments,
    HfArgumentParser,
)

from robust_deid.ner_datasets import DatasetCreator
from robust_deid.sequence_tagging import SequenceTagger
from robust_deid.sequence_tagging.arguments import (
    ModelArguments,
    DataTrainingArguments,
    EvaluationArguments,
)
from robust_deid.deid import TextDeid

class App(object):
    
    def __init__(
        self,
        model,
        threshold,
        span_constraint='super_strict',
        sentencizer='en_core_sci_sm',
        tokenizer='clinical',
        max_tokens=128,
        max_prev_sentence_token=32,
        max_next_sentence_token=32,
        default_chunk_size=32,
        ignore_label='NA'
    ):
        # Create the dataset creator object
        self._dataset_creator = DatasetCreator(
            sentencizer=sentencizer,
            tokenizer=tokenizer,
            max_tokens=max_tokens,
            max_prev_sentence_token=max_prev_sentence_token,
            max_next_sentence_token=max_next_sentence_token,
            default_chunk_size=default_chunk_size,
            ignore_label=ignore_label
        )
        parser = HfArgumentParser((
        ModelArguments,
        DataTrainingArguments,
        EvaluationArguments,
        TrainingArguments
        ))
        model_config = App._get_model_config()
        model_config['model_name_or_path'] = App._get_model_map()[model]
        if threshold == 'No threshold':
            model_config['post_process'] = 'argmax'
            model_config['threshold'] = None
        else:
            model_config['post_process'] = 'threshold_max'
            model_config['threshold'] = \
            App._get_threshold_map()[model_config['model_name_or_path']][threshold]
        print(model_config)
        #sys.exit(0)
        with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
            tmp.write(json.dumps(model_config) + '\n')
            tmp.seek(0)
            # If we pass only one argument to the script and it's the path to a json file,
            # let's parse it to get our arguments.
            self._model_args, self._data_args, self._evaluation_args, self._training_args = \
            parser.parse_json_file(json_file=tmp.name)
        # Initialize the text deid object
        self._text_deid = TextDeid(notation=self._data_args.notation, span_constraint=span_constraint)
        # Initialize the sequence tagger
        self._sequence_tagger = SequenceTagger(
            task_name=self._data_args.task_name,
            notation=self._data_args.notation,
            ner_types=self._data_args.ner_types,
            model_name_or_path=self._model_args.model_name_or_path,
            config_name=self._model_args.config_name,
            tokenizer_name=self._model_args.tokenizer_name,
            post_process=self._model_args.post_process,
            cache_dir=self._model_args.cache_dir,
            model_revision=self._model_args.model_revision,
            use_auth_token=self._model_args.use_auth_token,
            threshold=self._model_args.threshold,
            do_lower_case=self._data_args.do_lower_case,
            fp16=self._training_args.fp16,
            seed=self._training_args.seed,
            local_rank=self._training_args.local_rank
        )
        # Load the required functions of the sequence tagger
        self._sequence_tagger.load()
        
            
    def get_ner_dataset(self, notes_file):
        ner_notes = self._dataset_creator.create(
            input_file=notes_file,
            mode='predict',
            notation=self._data_args.notation,
            token_text_key='text',
            metadata_key='meta',
            note_id_key='note_id',
            label_key='label',
            span_text_key='spans'
        )
        return ner_notes
    
    def get_predictions(self, ner_notes_file):
        # Set the required data and predictions of the sequence tagger
        # Can also use self._data_args.test_file instead of ner_dataset_file (make sure it matches ner_dataset_file)
        self._sequence_tagger.set_predict(
            test_file=ner_notes_file,
            max_test_samples=self._data_args.max_predict_samples,
            preprocessing_num_workers=self._data_args.preprocessing_num_workers,
            overwrite_cache=self._data_args.overwrite_cache
        )
        # Initialize the huggingface trainer
        self._sequence_tagger.setup_trainer(training_args=self._training_args)
        # Store predictions in the specified file
        predictions = self._sequence_tagger.predict()
        return predictions
    
    def get_deid_text_removed(self, notes_file, predictions_file):
        deid_notes = self._text_deid.run_deid(
            input_file=notes_file,
            predictions_file=predictions_file,
            deid_strategy='remove',
            keep_age=False,
            metadata_key='meta',
            note_id_key='note_id',
            tokens_key='tokens',
            predictions_key='predictions',
            text_key='text',
        )
        return deid_notes
    
    def get_deid_text_replaced(self, notes_file, predictions_file):
        deid_notes = self._text_deid.run_deid(
            input_file=notes_file,
            predictions_file=predictions_file,
            deid_strategy='replace_informative',
            keep_age=False,
            metadata_key='meta',
            note_id_key='note_id',
            tokens_key='tokens',
            predictions_key='predictions',
            text_key='text',
        )
        return deid_notes
    
    
    @staticmethod
    def _get_highlights(deid_text):
        pattern = re.compile('<<(PATIENT|STAFF|AGE|DATE|LOCATION|PHONE|ID|EMAIL|PATORG|HOSPITAL|OTHERPHI):(.)*?>>')
        tag_pattern = re.compile('<<(PATIENT|STAFF|AGE|DATE|LOCATION|PHONE|ID|EMAIL|PATORG|HOSPITAL|OTHERPHI):')
        text_list = []
        current_start = 0
        current_end = 0
        for match in re.finditer(pattern, deid_text):
            full_start, full_end = match.span()
            sub_text = deid_text[full_start:full_end]
            sub_match = re.search(tag_pattern, sub_text)
            sub_span = sub_match.span()
            tag_length = sub_match.span()[1] - sub_match.span()[0]
            yield (deid_text[current_start:full_start], None)
            yield (deid_text[full_start+sub_span[1]:full_end-2], sub_match.string[sub_span[0]+2:sub_span[1]-1])
            current_start = full_end
        yield (deid_text[full_end:], None)
    
    @staticmethod
    def _get_model_map():
        return {
            'OBI-RoBERTa De-ID':'obi/deid_roberta_i2b2',
            'OBI-ClinicalBERT De-ID':'obi/deid_bert_i2b2'
        }
    
    @staticmethod
    def _get_threshold_map():
        return {
            'obi/deid_bert_i2b2':{"99.5": 4.656325975101986e-06, "99.7":1.8982457699258832e-06},
            'obi/deid_roberta_i2b2':{"99.5": 2.4362972672812125e-05, "99.7":2.396420546444644e-06}
        }
    
    @staticmethod
    def _get_model_config():
        return {
            "post_process":None,
            "threshold": None,
            "model_name_or_path":None,
            "task_name":"ner",
            "notation":"BILOU",
            "ner_types":["PATIENT", "STAFF", "AGE", "DATE", "PHONE", "ID", "EMAIL", "PATORG", "LOC", "HOSP", "OTHERPHI"],
            "truncation":True,
            "max_length":512,
            "label_all_tokens":False,
            "return_entity_level_metrics":True,
            "text_column_name":"tokens",
            "label_column_name":"labels",
            "output_dir":"./run/models",
            "logging_dir":"./run/logs",
            "overwrite_output_dir":False,
            "do_train":False,
            "do_eval":False,
            "do_predict":True,
            "report_to":[],
            "per_device_train_batch_size":0,
            "per_device_eval_batch_size":16,
            "logging_steps":1000
        }

def deid(text, model, threshold):
    notes = [{"text": text, "meta": {"note_id": "note_1", "patient_id": "patient_1"}, "spans": []}]
    app = App(model, threshold)
    # Create temp notes file
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        for note in notes:
            tmp.write(json.dumps(note) + '\n')
        tmp.seek(0)
        ner_notes = app.get_ner_dataset(tmp.name)
    # Create temp ner_notes file    
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        for ner_sentence in ner_notes:
            tmp.write(json.dumps(ner_sentence) + '\n')
        tmp.seek(0)
        predictions = app.get_predictions(tmp.name)
    # Get deid text
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp,\
    tempfile.NamedTemporaryFile("w+", delete=False) as tmp_1:
        for note in notes:
            tmp.write(json.dumps(note) + '\n')
        for note_prediction in predictions:
            tmp_1.write(json.dumps(note_prediction) + '\n')
        tmp.seek(0)
        tmp_1.seek(0)
        deid_text = list(app.get_deid_text_replaced(tmp.name, tmp_1.name))[0]['deid_text']
        deid_text_remove = list(app.get_deid_text_removed(tmp.name, tmp_1.name))[0]['deid_text']
    return [highlight_text for highlight_text in App._get_highlights(deid_text)], deid_text_remove

recall_choices = ["No threshold", "99.5", "99.7"]
recall_radio_input = gr.inputs.Radio(recall_choices, type="value", default='No threshold', label='RECALL THRESHOLD')

model_choices = list(App._get_model_map().keys())
model_radio_input = gr.inputs.Radio(model_choices, type="value", default='OBI-RoBERTa De-ID', label='DE-ID MODEL')

title = 'DE-IDENTIFICATION OF ELECTRONIC HEALTH RECORDS'
description = 'Models to remove private information (PHI/PII) from raw medical notes. The recall threshold (bias) can be used to remove PHI more aggressively.'

gradio_input = gr.inputs.Textbox(
    lines=10,
    placeholder='Enter text with PHI',
    label='RAW MEDICAL NOTE'
)

gradio_highlight_output = gr.outputs.HighlightedText(
    label='LABELED DE-IDENTIFIED MEDICAL NOTE',
)

gradio_text_output = gr.outputs.Textbox(
    label='DE-IDENTIFIED MEDICAL NOTE'
)

examples = [["Physician Discharge Summary Admit date: 10/12/1982 Discharge date: 10/22/1982 Patient Information Jack Reacher, 54 y.o. male (DOB = 1/21/1928). Home Address: 123 Park Drive, San Diego, CA, 03245. Home Phone: 202-555-0199 (home). Hospital Care Team Service: Orthopedics Inpatient Attending: Roger C Kelly, MD Attending phys phone: (634)743-5135 Discharge Unit: HCS843 Primary Care Physician: Hassan V Kim, MD 512-832-5025.", "OBI-RoBERTa De-ID", "No threshold"], ["Consult NotePt: Ulysses Ogrady MC #0937884Date: 07/01/19 Williams Ct M OSCAR, JOHNNY Hyderabad, WI 62297\n\nHISTORY OF PRESENT ILLNESS: The patient is a 77-year-old-woman with long standing hypertension who presented as a Walk-in to me at the Brigham Health Center on Friday. Recently had been started q.o.d. on Clonidine since 01/15/19 to taper off of the drug. Was told to start Zestril 20 mg. q.d. again. The patient was sent to the Unit for direct admission for cardioversion and anticoagulation, with the Cardiologist, Dr. Wilson to follow.\nSOCIAL HISTORY: Lives alone, has one daughter living in Nantucket. Is a non-smoker, and does not drink alcohol.\nHOSPITAL COURSE AND TREATMENT: During admission, the patient was seen by Cardiology, Dr. Wilson, was started on IV Heparin, Sotalol 40 mg PO b.i.d. increased to 80 mg b.i.d., and had an echocardiogram. By 07-22-19 the patient had better rate control and blood pressure control but remained in atrial fibrillation. On 08.03.19, the patient was felt to be medically stable.", "OBI-RoBERTa De-ID", "99.5"], ["Consult NotePt: Ulysses Ogrady MC #0937884Date: 07/01/19 Williams Ct M OSCAR, JOHNNY Hyderabad, WI 62297\n\nHISTORY OF PRESENT ILLNESS: The patient is a 77-year-old-woman with long standing hypertension who presented as a Walk-in to me at the Brigham Health Center on Friday. Recently had been started q.o.d. on Clonidine since 01/15/19 to taper off of the drug. Was told to start Zestril 20 mg. q.d. again. The patient was sent to the Unit for direct admission for cardioversion and anticoagulation, with the Cardiologist, Dr. Wilson to follow.\nSOCIAL HISTORY: Lives alone, has one daughter living in Nantucket. Is a non-smoker, and does not drink alcohol.\nHOSPITAL COURSE AND TREATMENT: During admission, the patient was seen by Cardiology, Dr. Wilson, was started on IV Heparin, Sotalol 40 mg PO b.i.d. increased to 80 mg b.i.d., and had an echocardiogram. By 07-22-19 the patient had better rate control and blood pressure control but remained in atrial fibrillation. On 08.03.19, the patient was felt to be medically stable.", "OBI-ClinicalBERT De-ID", "99.5"], ['HPI: Pt is a 59 yo Khazakhstani male, with who was admitted to San Rafael Mount Hospital following a syncopal nauseas and was brought to Rafael Mount ED. Five weeks ago prior Anemia: On admission to Rafael Hospital, Hb/Hct: 11.6/35.5. Tobacco: Quit at 38 y/o; ETOH: 1-2 beers/week; Caffeine:\nDD:05/05/2022 DT:05/05/2022 WK:65255 :4653\nNO GROWTH TO DATE Specimen: 38:Z8912708G Collected\n\n2nd set biomarkers (WPH): Creatine Kinase Isoenzymes Hospitalized 2115 TCH for ROMI 2120 TCH new onset\n\nLab Tests Amador: the lab results show good levels of 10MG PO qd : 04/10/2021 - 05/15/2021 ACT : rosenberg 128\n placed 3/22 for bradycardia. P/G model #5435, serial # 4712198. \n\nSocial history: Married, glazier, 3 grown adult children. Has VNA. Former civil engineer, supervisor, consultant. She is looking forward to a good Christmas. She is here today',
 "OBI-ClinicalBERT De-ID", 'No threshold']]

iface = gr.Interface(
    title=title,
    description=description,
    theme='huggingface',
    layout='horizontal',
    examples=examples,
    fn=deid,
    inputs=[gradio_input, model_radio_input, recall_radio_input],
    outputs=[gradio_highlight_output, gradio_text_output],
)
iface.launch()