import dspy
import os
import ast
import pandas as pd
from dotenv import load_dotenv
from dspy.teleprompt import BootstrapFewShot
from dspy.evaluate.evaluate import Evaluate
from app.core.persona_crafting import PersonaCrafting

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")

STUDENT_MODEL_NAME = "gemini/gemini-2.5-flash-preview-05-20"
TEACHER_MODEL_NAME = "gemini-2.5-flash-preview-05-20"
DATASET_PATH = "data/examples/phase1_persona_crafting.jsonl"
OPTIMIZED_STUDENT_MODEL_SAVE_PATH = "models/optimized_persona_crafting_student.json"

student_lm = dspy.LM(model=STUDENT_MODEL_NAME, api_key=GEMINI_API_KEY)
teacher_lm = dspy.LM(model=TEACHER_MODEL_NAME, api_key=GEMINI_API_KEY)

dspy.settings.configure(lm=student_lm)

df = pd.read_json(DATASET_PATH, lines=True)
dataset = []

for _, row in df.iterrows():
    example = dspy.Example(
        inferred_user_style=row['inferred_user_style'],
        emotional_tone=row['emotional_tone'],
        persona_hints=row['persona_hints'],
        short_term_conversation_history=row['short_term_conversation_history'],
        chatbot_persona_description=row['chatbot_persona_description'],
        response_style_guide=row['response_style_guide']
    ).with_inputs('inferred_user_style', 'emotional_tone', 'persona_hints', 'short_term_conversation_history')
    dataset.append(example)

train_size = int(0.5 * len(dataset))
trainset = dataset[:train_size]
devset = dataset[train_size:]

print(f"Loaded {len(dataset)} examples from {DATASET_PATH}")
print(f"Trainset size: {len(trainset)}, Devset size: {len(devset)}")
if not trainset:
    raise ValueError("Trainset is empty. Check dataset path and content.")

def validate_output(gold, pred, trace=None):
    """Simple metric: checks if all gold fields are present in pred and are non-empty."""
    if not all([
        pred.get('chatbot_persona_description'),
        pred.get('response_style_guide')
    ]):
        return False
    return True

teleprompter = BootstrapFewShot(
    metric=validate_output,
    max_bootstrapped_demos=4,  
    max_labeled_demos=5,       
    max_rounds=5              
)

optimized_persona_crafting = teleprompter.compile(
    student=PersonaCrafting(),
    trainset=trainset
)

print("Compilation complete.")

evaluator = Evaluate(
    devset=devset,
    metric=validate_output,
    num_threads=1,
    display_progress=True,
    display_table=5
)

evaluation_results = evaluator(optimized_persona_crafting)
print(f"Evaluation results: {evaluation_results}")

try:
    optimized_persona_crafting.save(OPTIMIZED_STUDENT_MODEL_SAVE_PATH)
    print(f"Optimized model saved to {OPTIMIZED_STUDENT_MODEL_SAVE_PATH}")
except Exception as e:
    print(f"Error saving the optimized model: {e}")

print("Optimization script finished.")
