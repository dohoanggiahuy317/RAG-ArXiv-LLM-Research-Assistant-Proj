from sentence_transformers import InputExample
import json
from torch.utils.data import DataLoader
from sentence_transformers import losses
from sentence_transformers import SentenceTransformer

import argparse


# Load data
def load_input_example(dataset_path):
    f = open(dataset_path)
    data = json.load(f)

    # Init empty train
    data_train = []

    # Parse data in
    for i in range(len(data)):
        example = data[i]   

        for pos in example["pos"]:
            data_train.append(
            InputExample(
                texts=[
                    example['query'], 
                    pos,  
                ] 
            ))

    return data_train


# Train model function 
def train_model(model_name, data_train, epoch, batch_size, device, shuffle = True):
    train_dataloader = DataLoader(data_train, shuffle=shuffle, batch_size=batch_size)
    model = SentenceTransformer(model_name, device = device)
    # train_loss = losses.TripletLoss(model=model)
    train_loss = losses.MultipleNegativesRankingLoss(model=model)
    model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=epoch) 
    return model


def main():
    device = "cuda"

    parser = argparse.ArgumentParser(description='Finetune the embedding vectors')
    parser.add_argument('--dataset_train_path', type=str, help='Dataset File path')
    parser.add_argument('--model_name', type=str, help='Dataset File path')
    parser.add_argument('--epoch', type=int, help='epoch', default=10)
    parser.add_argument('--batch_size', type=int, help='batch_size', default=16)
    parser.add_argument('--model_path', type=str, help='Dataset File path')

    args = parser.parse_args()

    # load train format
    data_train = load_input_example(args.dataset_train_path)

    # Fine tune
    model = train_model(
        model_name=args.model_name, 
        data_train=data_train, 
        epoch=args.epoch,
        batch_size=args.batch_size,
        device=device)
    
    model.save(args.model_path)

main()
    