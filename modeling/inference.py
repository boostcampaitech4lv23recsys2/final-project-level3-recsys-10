import warnings
import os
import pandas as pd
import requests
from datetime import timezone, timedelta

from google.cloud import storage

import torch

from args import parse_args
from dataloader import load_data, get_db_engine, save_data_for_recbole
from utils import wandb_download, best_model_finder, subprocess_recbole, update_meta_data


def main(args):
    # basic settings
    warnings.filterwarnings('ignore')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./core/storage.json"
    storage_client = storage.Client()
    KST = timezone(timedelta(hours=9))
    engine = get_db_engine()
    
    # batch_tag update in db <<before inference>>
    if args.update_batch_tag:
        print('update batch tag & load data...')
        meta_data = pd.read_sql(f"select * from public.meta_data", engine)
        meta_data['batch_tag'] += 1
        update_meta_data(meta_data, engine)
        
        inter_df, _ = load_data()
        save_data_for_recbole(inter_df=inter_df)
        
        print('done')
        return
    
    engine = get_db_engine()
    meta_data = pd.read_sql(f"select * from public.meta_data", engine)
    batch_tag = meta_data['batch_tag'].item()
    args.batch_tag = batch_tag
    
    # best_model update in db <<after inference>>
    if args.inference_info:
        print('find best models...')
        run_df = wandb_download(str(args.batch_tag))
        best_model_names, best_model_scores = best_model_finder(run_df, top_n=3)
        
        meta_data['best_model'] = str(best_model_names)
        processed_best_model_score = list()
        for score in best_model_scores:
            processed_best_model_score.append(round(score * 1000, 4))
        beta = round(sum(processed_best_model_score), 4)
        processed_best_model_score.extend([beta - processed_best_model_score[i] for i in range(len(best_model_scores))])

        meta_data['inference_traffic'] = str(processed_best_model_score)
        update_meta_data(meta_data, engine)
        
        requests.post(f"http://next-hanggi.kro.kr:30002/api/v1/updatemodel", json= {"qeury": "inference done.", "user_factor": "string", "item_factor": "string"})
        
        print('done.')
        return

    # model inference
    device = "cuda" if torch.cuda.is_available() else "cpu"
    saved = os.path.join('/opt/ml/final-project-level3-recsys-13/modeling/RecBole/saved', str(args.batch_tag))
    bucket = storage_client.bucket('foodcom_als_model')
        
    if args.model == 'BPR':
        subprocess_recbole(model_name=args.model, batch_tag=batch_tag, path=saved)
        print('uploading...')
        bucket.blob(f'{args.model}.npy').upload_from_filename(os.path.join(saved, f'{args.model}.npy'))
        
        print(f'{args.model} done.')
        
    elif args.model == 'LightGCN':
        subprocess_recbole(model_name=args.model, batch_tag=batch_tag, path=saved)
        print('uploading...')
        bucket.blob(f'{args.model}.npy').upload_from_filename(os.path.join(saved, f'{args.model}.npy'))
        
        print(f'{args.model} done.')
        
    elif args.model == 'MultiVAE':
        subprocess_recbole(model_name=args.model, batch_tag=batch_tag, path=saved)
        print('uploading...')
        bucket.blob(f'{args.model}.npy').upload_from_filename(os.path.join(saved, f'{args.model}.npy'))
        
        print(f'{args.model} done.')
        
    elif args.model == 'MultiDAE':
        subprocess_recbole(model_name=args.model, batch_tag=batch_tag, path=saved)
        print('uploading...')
        bucket.blob(f'{args.model}.npy').upload_from_filename(os.path.join(saved, f'{args.model}.npy'))
        
        print(f'{args.model} done.')
        
    elif args.model == 'CDAE':
        subprocess_recbole(model_name=args.model, batch_tag=batch_tag, path=saved)
        print('uploading...')
        bucket.blob(f'{args.model}.npy').upload_from_filename(os.path.join(saved, f'{args.model}.npy'))
        
        print(f'{args.model} done.')
        
    elif args.model == 'RecVAE':
        subprocess_recbole(model_name=args.model, batch_tag=batch_tag, path=saved)
        print('uploading...')
        bucket.blob(f'{args.model}.npy').upload_from_filename(os.path.join(saved, f'{args.model}.npy'))
        
        print(f'{args.model} done.')
            

if __name__ == "__main__": 
    args = parse_args()
    main(args)