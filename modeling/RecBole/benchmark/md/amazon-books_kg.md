# Amazon-Books(2018) Sequential

**Dataset:** amazon-books_seq

**Data filtering:** delete interactive records with rating less than 3

**K-core filtering:** delete inactive users or unpopular items with less than 10 interactions

**Evaluation method:** chronological arrangement, leave one out split data set and full sorting

**Evaluation metric:** Recall@10, NGCG@10, MRR@10, Hit@10, Precision@10

## Dataset Information

| Dataset      | #User    | #Item  | #Interactions | Sparsity | #Entity | #Relation | #Triple  |
|--------------|----------|--------|---------------|----------|---------|-----------|----------|
| amazon-books | 160,383  | 4,000  | 344,601       | 99.9463% | 10,302  | 22        | 152,882  |

**Configuration file (amazon-books_seq.yaml):**

```yaml
# dataset config
field_separator: "\t"
seq_separator: " "
USER_ID_FIELD: user_id
ITEM_ID_FIELD: item_id
RATING_FIELD: rating
HEAD_ENTITY_ID_FIELD: head_id
TAIL_ENTITY_ID_FIELD: tail_id
RELATION_ID_FIELD: relation_id
ENTITY_ID_FIELD: entity_id
NEG_PREFIX: neg_
LABEL_FIELD: label
load_col:
    inter: [user_id, item_id, rating]
    kg: [head_id, relation_id, tail_id]
    link: [item_id, entity_id]

# data filtering for interactions
val_interval:
    rating: "[3,inf)"    
unused_col: 
    inter: [rating]

user_inter_num_interval: "[10,inf)"
item_inter_num_interval: "[10,inf)"

# data preprocessing for knowledge graph triples
kg_reverse_r: True
entity_kg_num_interval: "[5,inf)"
relation_kg_num_interval: "[5,inf)"

# training and evaluation
epochs: 500
train_batch_size: 4096
eval_batch_size: 40960000
valid_metric: NDCG@10
train_neg_sample_args: 
    distribution: uniform
    sample_num: 1
    dynamic: False

```

## Note

- In order to ensure fairness between models, we limit the embedding dimension of users and items to `64`. Please adjust the parameter name in different models.

  ```yaml
  embedding_size: 64 
  ```

