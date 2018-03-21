# Keras2 ChainCRF Fix

Models based on LSTM and Conditional Random Fields (CRF) can obtain State of the Art results on sequence labelling tasks in Natual Language Processing, such as Named Entity Recognition (NER), Part of Speech (POS) and Chunking `[1, 2]`.

<<<<<<< HEAD
Despite of this, there is no official implementation of a CRF layer, more specifically Chain CRF, available on Keras. Currently there's one implementation on [keras-contrib](https://github.com/keras-team/keras-contrib/blob/master/keras_contrib/layers/crf.py)  (example of usage [here](https://github.com/keras-team/keras-contrib/blob/master/examples/conll2000_chunking_crf.py)) by [linxihui](https://github.com/linxihui) and another one kindly provided by [phipleg](https://github.com/phipleg) (an extensive merge discussion thread can be found [here)](https://github.com/keras-team/keras/issues/4090#issuecomment-374646730). Unfortunatelly the latter implementation doesn't work on the most recent versions of Keras 2, although such limitation can be easily overcome by modifying two lines of code, as shown by [Hironsan](https://github.com/Hironsan) on [this commit](https://github.com/Hironsan/anago/commit/febaa4757e0cf3a3dd51f93fe62f30d637e2afea).

The goal of this repository consists in showing which changes have to be made in the code kindly developed by phipleg and contributors, so it can work on the most recent version of Keras (currently 2.1.5); and to provide a minimum working example of a CRF-based model for POS tagging.

The present implementation is inspired on the code developed by [nreimers](https://github.com/nreimers), [emnlp2017-bilstm-cnn-crf](https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf) `[3]`.



### Installing and running

To execute this demo just run `pip install -r requirements.txt`, then download the word embeddings by running `./get_embeddings.sh` and the dataset for POS tagging with `./get_data.sh`, finally run the notebook `crf_versions.ipynb`. Please bear in mind that you can see the results by just checking the notebook instead. To see which modifications have to be made on the ChainCRF code, please refer to the commit`18ed5b9 CRF layer works with Keras 2+.`.



### References

[1] Lample, Guillaume, et al. "Neural architectures for named entity recognition." *arXiv preprint arXiv:1603.01360* (2016).

[2] Ma, Xuezhe, and Eduard Hovy. "End-to-end sequence labeling via bi-directional lstm-cnns-crf." *arXiv preprint arXiv:1603.01354* (2016).

[3] Reimers, Nils, and Iryna Gurevych. "Reporting score distributions makes a difference: Performance study of lstm-networks for sequence tagging." *arXiv preprint arXiv:1707.09861* (2017).

