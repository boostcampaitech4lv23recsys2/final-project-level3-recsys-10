import os
import torch
import pandas as pd
import wandb
from args import parse_args
import warnings
from datetime import datetime, timezone, timedelta

import sqlalchemy
from dataloader import get_db_engine

import foodcomTorch
import foodcomImplicit
from foodcomItem2Vec.bert2vec import bert2vec

from utils import setSeeds

def main(args):

    # basic settings
    setSeeds(args.seed)
    args.device = device
    
    engine = get_db_engine()
    meta_data = pd.read_sql(f"select * from public.meta_data", engine)
    batch_tag = meta_data['batch_tag'].item()
    args.batch_tag = batch_tag

    # model
    if args.model == "als":
        wandb.login()
        wandb.init(project='foodcom')
        
        now = datetime.now(KST).strftime('%Y-%m-%d_%H:%M:%S')
        print(f'als ! [start time: {now}]')
        train_data, user_item_matrix, test_data = foodcomImplicit.dataset.read_data(args)
        foodcomImplicit.trainer.run(args, train_data, user_item_matrix, test_data)
        
    elif args.model == 'torch-':
        pass
    
        # preprocess = foodcomTorch.Preprocess_interactions(args)
        # preprocess.load_train_data(args.file_name)
        # train_data = preprocess.get_train_data()
        # train_data, valid_data = preprocess.split_data(train_data)
        # foodcomTorch.run(args, train_data, valid_data)
        
    elif args.model == 'bert2vec':
        bert2vec(args)
        
    

if __name__ == "__main__":    
    args = parse_args()
    main(args)