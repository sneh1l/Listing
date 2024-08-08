import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import MBart50TokenizerFast, MBartForSequenceClassification 
import warnings 
warnings.filterwarnings('ignore')


device = torch.device( 
    'cuda') if torch.cuda.is_available() else torch.device('cpu')

#more language can be added here
get_lang_code = {
    "hi":"hi_IN",
    "en":"en_XX"
}

model_name = "kumarsushant36/multiLingual_Toxic_Text_Classification"
Bart_Tokenizer = MBart50TokenizerFast.from_pretrained(model_name) 
Bart_Model = MBartForSequenceClassification.from_pretrained( 
model_name).to(device)

def predict_user_input(input_text, lang, model=Bart_Model, tokenizer=Bart_Tokenizer, device=device): 
    if lang not in get_lang_code:
        return None
    

    user_input = [input_text] 

    tokenizer.src_lang = get_lang_code[lang]
    user_encodings = tokenizer( 
        user_input, truncation=True, padding=True, return_tensors="pt") 

    user_dataset = TensorDataset( 
        user_encodings['input_ids'], user_encodings['attention_mask']) 

    user_loader = DataLoader(user_dataset, batch_size=1, shuffle=False) 

    model.eval() 
    with torch.no_grad(): 
        for batch in user_loader: 
            input_ids, attention_mask = [t.to(device) for t in batch] 
            outputs = model(input_ids, attention_mask=attention_mask) 
            logits = outputs.logits 
            predictions = torch.sigmoid(logits) 

    predicted_labels = (predictions.cpu().numpy() > 0.5).astype(int) 
    labels_list = ['toxic', 'severe_toxic', 'obscene', 
                   'threat', 'insult', 'identity_hate'] 
    # result = dict(zip(labels_list, predicted_labels[0])) 
    result = [label for label, pred in zip(labels_list, predicted_labels[0]) if pred == 1]
    return result


text = "I will kill you"
src_lang = "en"
result = predict_user_input(input_text=text, lang=src_lang)
print(result)
