import torch
from torch.utils.data import TensorDataset
from transformers import BartForConditionalGeneration, BartTokenizer


class ModelCaller:
    model = None
    tokenizer = None

    def __init__(self):
        self.__init_model()

    def model_call(self, text):
        # call ml model with text.
        dataloader = self.__tokenize_input(text)
        _, summary = self.__generate_summary(dataloader, len(text))
        return summary

    def __init_model(self, device='cpu'):
        self.model = BartForConditionalGeneration.from_pretrained('facebook/bart-base').to(
            device)  # use uncased, so it doesn't care about upper vs lower case
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')

        self.model.load_state_dict(torch.load("./app/model/obj/model_full_bart_epoch_3.pt",
                                              map_location=torch.device(device)), strict=False)
        self.model.to(device)

    def __tokenize_input(self, text):

        text = [text.strip().replace("\n", "")]
        tokenized_input = self.tokenizer(text, padding='longest', truncation=True, return_tensors='pt')

        input_ids, attention_mask = tokenized_input.input_ids, tokenized_input.attention_mask
        input_ids = input_ids.detach().clone()
        attention_mask = attention_mask.detach().clone()

        dataset = TensorDataset(input_ids, attention_mask)
        train_dataloader = torch.utils.data.DataLoader(dataset, batch_size=1)
        return train_dataloader

    def __generate_summary(self, text_input, n):
        with torch.no_grad():
            results = {}  # compile list of outputs
            for i, data in enumerate(text_input):
                input_ids, _ = data
                if n <= 45:
                    output = self.model.generate(input_ids,
                                                 num_beams=4,
                                                 max_length=n)
                else:
                    output = self.model.generate(input_ids,
                                                 num_beams=4,
                                                 no_repeat_ngram_size=2,
                                                 min_length=30,
                                                 max_length=100,
                                                 early_stopping=True)

                for original, summary in zip(input_ids, output):
                    results = (self.tokenizer.decode(original, skip_special_tokens=True),
                               self.tokenizer.decode(summary, skip_special_tokens=True))
        return results
