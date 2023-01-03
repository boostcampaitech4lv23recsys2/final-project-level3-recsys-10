
import os
import pickle
import ast
from datetime import datetime, timezone, timedelta

import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import numpy as np

from datalset import load_data
from utils import large_cosine_similarity


class CBModel(nn.Module):
    def __init__(self, args):
        super(CBModel, self).__init__()
        self.args = args
        self.device = args.device
        self.hidden_dim = self.args.hidden_dim

        self.embedding_item = nn.ModuleDict(
            {
                col: nn.Embedding(num + 1, self.hidden_dim // 3)
                for col, num in args.n_embeddings.items()
            }
        )

        num_item_cols = len(args.item_loc) + 1
        self.proj_1 = nn.Sequential(
            nn.Linear(self.hidden_dim // 3 * num_cate_cols, self.hidden_dim),
            nn.LayerNorm(self.hidden_dim),
        )

        self.embedding_infra = nn.Sequential(
            nn.Linear(len(args.infra_loc), self.hidden_dim),
            nn.LayerNorm(self.hidden_dim),
        )

        self.proj_2 = nn.Sequential(
            nn.Linear(self.args.hidden_dim * 2, self.args.hidden_dim),
        )
        
        # Encoder
        self.query = nn.Linear(in_features=self.hidden_dim, out_features=self.hidden_dim)
        self.key = nn.Linear(in_features=self.hidden_dim, out_features=self.hidden_dim)
        self.value = nn.Linear(in_features=self.hidden_dim, out_features=self.hidden_dim)

        self.attn = nn.MultiheadAttention(embed_dim=self.hidden_dim, num_heads=self.args.n_heads)
        
        self.ffn = Feed_Forward_block(self.hidden_dim)      

        self.ln1 = nn.LayerNorm(self.hidden_dim)
        self.ln2 = nn.LayerNorm(self.hidden_dim)

        # GRU
        self.gru = nn.GRU(
            self.hidden_dim, self.hidden_dim, self.args.n_layers, batch_first=True)

        # Fully connected layer
        self.fc = nn.Linear(self.hidden_dim, 1)
       
        self.activation = nn.Sigmoid()


    
    def forward(self, input):
        item_id, service, sales, deposit, rent, exclusive_area, supply_area, location, local, infra_1, infra_2, infra_3, infra_4, infra_5 = input

        

        q = self.query(embed).permute(1, 0, 2)
        # q = self.query(embed)[:, -1:, :].permute(1, 0, 2)

        k = self.key(embed).permute(1, 0, 2)
        v = self.value(embed).permute(1, 0, 2)

        ## attention
        out, _ = self.attn(q, k, v)
        
        ## residual + layer norm
        out = out.permute(1, 0, 2)
        out = embed + out
        out = self.ln1(out)

        ## feed forward network
        out = self.ffn(out)

        ## residual + layer norm
        out = embed + out
        out = self.ln2(out)

        
        ###################### GRU #####################
        hidden = self.init_hidden(batch_size)
        out, hidden = self.gru(out, hidden[0])

        ###################### DNN #####################
        out = out.contiguous().view(batch_size, -1, self.hidden_dim)
        out = self.fc(out)

        preds = self.activation(out).view(batch_size, -1)

        return preds



