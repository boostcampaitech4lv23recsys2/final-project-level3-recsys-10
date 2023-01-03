import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    
    # cuda setting
    parser.add_argument("--device", default='cuda', type=str, help="cuda or cpu")
    
    # inference settings
    parser.add_argument("--inference_info", action='store_true')  # 해당 인자를 입력하면 True로 작용하여 best모델 정보 업데이트
    parser.add_argument("--update_batch_tag", action='store_true')  # 해당 인자를 입력하면 True로 작용하여 db의 batch tag 숫자 업데이트
    
    
    ## make subparsers
    subparsers = parser.add_subparsers(dest='model')
    parser_als = subparsers.add_parser(name='als')
    parser_bert2vec = subparsers.add_parser(name='bert2vec')
    parser_BPR = subparsers.add_parser(name='BPR')
    parser_LightGCN = subparsers.add_parser(name='LightGCN')
    parser_MultiVAE = subparsers.add_parser(name='MultiVAE')
    parser_MultiDAE = subparsers.add_parser(name='MultiDAE')
    parser_CDAE = subparsers.add_parser(name='CDAE')
    parser_RecVAE = subparsers.add_parser(name='RecVAE')
    
    # als settings
    parser_als.add_argument("--n_epochs", default=5, type=int, help="iter n")
    parser_als.add_argument("--patience", default=3, type=int, help="patient n. for early stopping")
    parser_als.add_argument("--no_exp_save", action='store_true')  # 해당 인자를 입력할 때만 True로 적용하여 실험 결과를 저장하지 않음
    parser_als.add_argument("--seed", default=42, type=int, help="seed")
    parser_als.add_argument("--n_valid", default=1, type=int, help="validation set n")
    parser_als.add_argument("--n_iter", default=20, type=int, help='iter in model')
    parser_als.add_argument("--n_seq", default=1, type=int, help="sequence n in the validation set")
    parser_als.add_argument("--factors", default=100, type=int, help="number of factors")
    parser_als.add_argument("--regularization", default=0.001, type=float, help="regularization")
    parser_als.add_argument("--als_dir",default="./foodcomImplicit/architects",type=str,help="als architects directory")
    parser_als.add_argument("--top_k", default=3, type=int, help="recall at k")
    parser_als.add_argument("--inference_n", default=10, type=int, help="argprtition n for inference")
    
    # bert2vec settings
    parser_bert2vec.add_argument("--seed", default=42, type=int, help="seed")
    parser_bert2vec.add_argument('--bert', type=str, default='bert-large-nli-stsb-mean-tokens', help='pretrained 모델')
    parser_bert2vec.add_argument('--save_path', type=str, default='./foodcomItem2Vec', help='similar_answer 저장위치')
    parser_bert2vec.add_argument("--cal_similarity", action='store_true')  # 해당 인자를 입력할 때만 True로 적용하여 실험 결과를 저장하지 않음
    parser_bert2vec.add_argument('--batch', type=int, default=2000, help='cosine_similarity 계산시 batch')
    parser_bert2vec.add_argument('--top_n', type=int, default=25, help='cosine_similarity에서 가져올 개수')
    parser_bert2vec.add_argument('--col_name1', type=str, default='recipes1', help='첫 번째 col 이름')
    parser_bert2vec.add_argument('--col_name2', type=str, default='recipes2', help='두 번째 col 이름')
        
    
    args = parser.parse_args()

    return 