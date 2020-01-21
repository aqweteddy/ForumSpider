from torch.utils.data import Dataset, DataLoader
import torch


class QuestDataset(Dataset):
    def __init__(self, df, tokenizer, input_categories, output_categories):
        self.tokenizer = tokenizer
        self.ids_q, self.masks_q, self.segs_q  = [], [], []
        self.ids_a, self.masks_a, self.segs_a  = [], [], []
        self.df = df
        self.output_categories = output_categories
        for _, inst in tqdm(df[input_categories]):
            title, question, answer = inst.question_title, inst.question_body, inst.answer
            
            id_q, mask_q, seg_q = self.encode_str(f'{title} {text}', None)
            id_a, mask_a, seg_a = self.encode_str(answer, None)
            
            self.ids_q.append(id_q)
            self.masks_q.append(mask_q)
            self.segs_q.append(seg_q)
            self.ids_a.append(id_a)
            self.masks_a.append(mask_a)
            self.segs_a.append(seg_a)

    def __getitem__(self, k):
        """
        return (id_q, mask_q, seg_q), (id_a, mask_a, seg_a), (OUTPUT)
        """
        return [torch.tensor(self.ids_q[k]), torch.tensor(self.masks_q[k]), torch.tensor(self.segs_a[k])],
               [torch.tensor(self.ids_a[k]), torch.tensor(self.masks_a[k]), torch.tensor(self.segs_a[k])],
               [torch.tensor(df[output_categories][k])]
                        

        
    
    def encode_str(s1, s2, truncation_strategy='longest_first', length=MAX_SEQ_LEN):
        inputs = self.tokenizer.encode_plus(str1, str2,
                                       add_special_tokens=True,
                                       max_length=length,
                                       truncation_strategy=truncation_strategy)

        pad_len = length - len(input_ids)
        pad_id = tokenizer.pad_token_id

#         data + padding
        input_id = inputs["input_ids"] + [pad_id] * pad_len
        input_mask = [1] * len(input_ids) + [0] * pad_len
        input_segment = inputs["token_type_ids"] + [0] * pad_len
        
        return [input_id, input_mask, input_segment]


