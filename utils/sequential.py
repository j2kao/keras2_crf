from collections import defaultdict

import numpy as np
from sklearn.preprocessing import LabelEncoder

class SequenceEncoder(LabelEncoder):
    def __init__(self):
        super().__init__()

    def fit(self, sequence):
        unique_items = set()
        for sample in sequence:
            unique_items.update(sample)

        super().fit(list(unique_items))
        return self

    def transform(self, sequence):
        f = super().transform
        return list([f(sample) for sample in sequence])

    def fit_transform(self, sequence):
        self.fit(sequence)
        return self.transform(sequence)


def batch_dataset(X, C, y, batch_size, show_details=0):
    # 1. organize sentence by length
    sequence_lens = defaultdict(list)
    for i, sequence in enumerate(X):
        sequence_lens[len(sequence)].append(i)

    # shows sentence lenght distribution
    entries = list(sequence_lens.items())
    if show_details == 2:
        entries = sorted(entries, key=lambda x: x[0])
        for length, sequences in entries:
            print('{}\t{}'.format(length, len(sequences)))
                        
    # 2. shuffling batches
    np.random.shuffle(entries)
    for sequence_len, sequence_indices in entries:
        # skipping 1-word sentences. Check code why....
        if sequence_len == 1:
            continue
        
        batch_samples_counter = 0
            
        # shuffling samples as well
        np.random.shuffle(sequence_indices)
        amount_sequences = len(sequence_indices)
        
        # the batch size is a soft-constraint and it is equalized
        # by the algorithm when the amount of samples is not a multiple
        # of the batch size, so each batch has roughtly the same amount
        # of samples.
        sequence_batches = int(np.ceil(amount_sequences / batch_size))
        sequence_batch_size = int(np.ceil(amount_sequences / sequence_batches))
        
        if show_details == 1:
            print('{} sentences with len {}'.format(amount_sequences, sequence_len))
            print('{} batches can be generated'.format(sequence_batches))
            print('each with {} samples'.format(sequence_batch_size))
        
        # creating the batches as a generator
        for batch in range(sequence_batches):
            
            lower = batch*sequence_batch_size            
            upper = (batch+1)*sequence_batch_size
            if upper > amount_sequences:
                upper = amount_sequences
                
            batch_samples_counter += (upper - lower)
                
            batch_indices = sequence_indices[lower:upper]
            X_batch = list()
            C_batch = list()
            y_batch = list()
            
            for index in batch_indices:
                X_batch.append(X[index])
                C_batch.append(C[index])
                y_batch.append(y[index]) # <<<
                
            y_batch = np.asarray(y_batch)
            y_batch = np.expand_dims(y_batch, -1)
            
            yield np.asarray(X_batch), np.asarray(C_batch), y_batch

        # at the end of this sequence generation, ensures that none was left behind
        assert(batch_samples_counter == amount_sequences)
